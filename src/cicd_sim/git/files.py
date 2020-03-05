class Files:
    """A collection of files
    
    Each file has a name (str) and content (str).
    """
    def __init__(self):
        self._files = {}
    
    def set_file_content(self, file_name, content):
        self._files[file_name] = content
    
    def get_file_content(self, file_name):
        if file_name in self._files:
            return self._files[file_name]
        return None
        