"""
File Service module.

Handles file uploads, storage, and management.
"""

import logging
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from typing import Optional

logger = logging.getLogger(__name__)


class FileService:
    """Service for file management."""
    
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp3', 'wav', 'mp4', 'pdf', 'txt'}
    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """Check if file type is allowed."""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in FileService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def save_file(file, user_id: int, file_type: str = 'general') -> Optional[str]:
        """
        Save uploaded file.
        
        Args:
            file: File object from request
            user_id: User ID for file organization
            file_type: Type of file (audio, document, etc.)
        
        Returns:
            File path relative to upload folder
        """
        try:
            if not file or file.filename == '':
                logger.error("No file selected")
                return None
            
            if not FileService.allowed_file(file.filename):
                logger.warning(f"File type not allowed: {file.filename}")
                return None
            
            if file.content_length > FileService.MAX_FILE_SIZE:
                logger.warning(f"File too large: {file.filename}")
                return None
            
            # Create user directory
            user_dir = os.path.join(FileService.UPLOAD_FOLDER, str(user_id), file_type)
            os.makedirs(user_dir, exist_ok=True)
            
            # Generate unique filename
            filename = secure_filename(file.filename)
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            filepath = os.path.join(user_dir, filename)
            file.save(filepath)
            
            logger.info(f"File saved: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            return None
    
    @staticmethod
    def delete_file(filepath: str) -> bool:
        """Delete a file."""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"File deleted: {filepath}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False
    
    @staticmethod
    def get_file_url(filepath: str) -> str:
        """Get public URL for file."""
        return f"/uploads/{filepath}"
    
    @staticmethod
    def cleanup_old_files(days: int = 30) -> int:
        """Delete files older than specified days."""
        try:
            from datetime import timedelta
            import time
            
            deleted_count = 0
            cutoff_time = time.time() - (days * 24 * 60 * 60)
            
            for root, dirs, files in os.walk(FileService.UPLOAD_FOLDER):
                for file in files:
                    filepath = os.path.join(root, file)
                    if os.path.getmtime(filepath) < cutoff_time:
                        os.remove(filepath)
                        deleted_count += 1
            
            logger.info(f"Cleanup complete: {deleted_count} old files deleted")
            return deleted_count
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            return 0
