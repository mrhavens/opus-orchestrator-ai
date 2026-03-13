"""S3/MinIO ingestion for Opus Orchestrator.

Fetches content from S3-compatible object storage.
"""

import os
import io
from typing import Any, Optional
from pathlib import Path

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv

load_dotenv("/home/solaria/.openclaw/workspace/opus-orchestrator-ai/.env")


class S3Ingestor:
    """Fetch and parse content from S3-compatible storage.
    
    Supports:
    - Amazon S3
    - MinIO
    - DigitalOcean Spaces
    - Wasabi
    - Other S3-compatible APIs
    """
    
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        region_name: str = "us-east-1",
        bucket: Optional[str] = None,
    ):
        """Initialize S3 ingestor.
        
        Args:
            endpoint_url: S3 endpoint URL (for MinIO, DO Spaces, etc.)
            access_key: AWS access key
            secret_key: AWS secret key
            region_name: AWS region
            bucket: Default bucket name
        """
        self.access_key = access_key or os.environ.get("AWS_ACCESS_KEY_ID")
        self.secret_key = secret_key or os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.endpoint_url = endpoint_url or os.environ.get("S3_ENDPOINT_URL")
        self.bucket = bucket
        
        if not self.access_key or not self.secret_key:
            raise ValueError(
                "S3 credentials required. Set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY "
                "or pass access_key/secret_key."
            )
        
        # Determine if using custom endpoint
        use_ssl = self.endpoint_url and not self.endpoint_url.startswith("http://")
        
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
        )
        
        self._buckets_cache: Optional[list[str]] = None

    def list_buckets(self) -> list[str]:
        """List available buckets.
        
        Returns:
            List of bucket names
        """
        try:
            response = self.s3_client.list_buckets()
            return [b["Name"] for b in response.get("Buckets", [])]
        except (ClientError, NoCredentialsError) as e:
            raise RuntimeError(f"Failed to list buckets: {e}")

    def list_objects(
        self,
        bucket: Optional[str] = None,
        prefix: str = "",
        max_keys: int = 1000,
    ) -> list[dict]:
        """List objects in a bucket.
        
        Args:
            bucket: Bucket name (uses default if not provided)
            prefix: Object key prefix filter
            max_keys: Maximum number of keys to return
            
        Returns:
            List of object metadata dicts
        """
        bucket = bucket or self.bucket
        if not bucket:
            raise ValueError("Bucket name required")
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix,
                MaxKeys=max_keys,
            )
            
            return [
                {
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "last_modified": obj.get("LastModified"),
                    "etag": obj.get("ETag", "").strip('"'),
                }
                for obj in response.get("Contents", [])
            ]
        except ClientError as e:
            raise RuntimeError(f"Failed to list objects: {e}")

    def get_object(
        self,
        key: str,
        bucket: Optional[str] = None,
        encoding: str = "utf-8",
    ) -> str:
        """Get content of a single object.
        
        Args:
            key: Object key
            bucket: Bucket name (uses default if not provided)
            encoding: Text encoding
            
        Returns:
            Object content as string
        """
        bucket = bucket or self.bucket
        if not bucket:
            raise ValueError("Bucket name required")
        
        try:
            response = self.s3_client.get_object(Bucket=bucket, Key=key)
            body = response["Body"]
            
            # Try to read as text
            content = body.read()
            try:
                return content.decode(encoding)
            except UnicodeDecodeError:
                # Return raw bytes as hex for binary files
                return f"[Binary file: {len(content)} bytes]"
                
        except ClientError as e:
            raise RuntimeError(f"Failed to get object {key}: {e}")

    def get_text_files(
        self,
        bucket: Optional[str] = None,
        prefix: str = "",
        extensions: Optional[list[str]] = None,
    ) -> dict[str, str]:
        """Get all text files from a prefix.
        
        Args:
            bucket: Bucket name
            prefix: Object key prefix
            extensions: File extensions to filter (e.g., ['.txt', '.md'])
            
        Returns:
            Dict mapping keys to content
        """
        bucket = bucket or self.bucket
        if not bucket:
            raise ValueError("Bucket name required")
        
        extensions = extensions or [".txt", ".md", ".markdown", ".notes", ".draft"]
        
        objects = self.list_objects(bucket=bucket, prefix=prefix)
        
        results = {}
        for obj in objects:
            key = obj["key"]
            
            # Check extension
            if not any(key.lower().endswith(ext) for ext in extensions):
                continue
            
            # Skip directories
            if key.endswith("/"):
                continue
            
            try:
                content = self.get_object(key, bucket)
                results[key] = content
            except Exception as e:
                print(f"Warning: Failed to read {key}: {e}")
                continue
        
        return results

    def ingest_bucket(
        self,
        bucket: Optional[str] = None,
        prefix: str = "",
        extensions: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Ingest all text content from a bucket/prefix.
        
        Args:
            bucket: Bucket name
            prefix: Object key prefix
            extensions: File extensions to include
            
        Returns:
            Dict with combined text and metadata
        """
        bucket = bucket or self.bucket
        if not bucket:
            raise ValueError("Bucket name required")
        
        files = self.get_text_files(
            bucket=bucket,
            prefix=prefix,
            extensions=extensions,
        )
        
        # Combine all content
        combined_lines = []
        for key, content in files.items():
            combined_lines.append(f"=== {key} ===")
            combined_lines.append(content)
            combined_lines.append("")
        
        combined_text = "\n".join(combined_lines)
        
        return {
            "bucket": bucket,
            "prefix": prefix,
            "files": files,
            "file_count": len(files),
            "total_chars": len(combined_text),
            "combined_text": combined_text,
        }

    def download_file(
        self,
        key: str,
        local_path: str | Path,
        bucket: Optional[str] = None,
    ) -> Path:
        """Download a file from S3 to local storage.
        
        Args:
            key: Object key
            local_path: Local destination path
            bucket: Bucket name
            
        Returns:
            Path to downloaded file
        """
        bucket = bucket or self.bucket
        if not bucket:
            raise ValueError("Bucket name required")
        
        local_path = Path(local_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.s3_client.download_file(bucket, key, str(local_path))
        
        return local_path

    def upload_file(
        self,
        local_path: str | Path,
        key: str,
        bucket: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> str:
        """Upload a file to S3.
        
        Args:
            local_path: Local file path
            key: Object key
            bucket: Bucket name
            content_type: Content MIME type
            
        Returns:
            S3 URL of uploaded file
        """
        bucket = bucket or self.bucket
        if not bucket:
            raise ValueError("Bucket name required")
        
        local_path = Path(local_path)
        
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type
        
        self.s3_client.upload_file(
            str(local_path),
            bucket,
            key,
            ExtraArgs=extra_args,
        )
        
        return f"s3://{bucket}/{key}"


def create_s3_ingestor(
    endpoint_url: Optional[str] = None,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    bucket: Optional[str] = None,
) -> S3Ingestor:
    """Factory function to create an S3 ingestor.
    
    Args:
        endpoint_url: S3 endpoint URL
        access_key: AWS access key
        secret_key: AWS secret key
        bucket: Default bucket
        
    Returns:
        Configured S3Ingestor
    """
    return S3Ingestor(
        endpoint_url=endpoint_url,
        access_key=access_key,
        secret_key=secret_key,
        bucket=bucket,
    )
