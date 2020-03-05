class SHA:
    """Represents a Git commit's SHA
    
    It does not actually calculate an SHA. Instead, it simply increments a 
    counter. This makes sense because the SHA makes it into the artifact name
    and therefore, the artifact's name tells the human "how old" it is. The 
    higher the SHA, the junger the artifact."""
    def __init__(self):
        self._counter = 0

    def generate_next(self):
        """@return the next (unique) SHA1 string of length 7"""
        self._counter += 1
        return self._format_sha(self._counter)

    def get_current(self):
        return self._format_sha(self._counter)

    def _format_sha(self, sha):
        return str(sha).zfill(7)