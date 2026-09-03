import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def __init__(self, image):
        """Initialize and convert grayscale images to RGB if needed."""
        #call parent constructor
        super(ResizeableImage, self).__init__(image)
        
        #check if image is grayscale and convert to RGB if needed
        sample_pixel = self[0, 0]
        if isinstance(sample_pixel, int):
            #convert all grayscale pixels to RGB tuples
            for j in range(self.height):
                for i in range(self.width):
                    gray_value = self[i, j]
                    self[i, j] = (gray_value, gray_value, gray_value)
    
    def best_seam(self, dp=True):
        """Returns the lowest-energy vertical seam as a list of coordinates.
        
        Args:
            dp: If True, uses dynamic programming. If False, uses naive recursion.
        
        Returns:
            List of (i, j) coordinates representing the seam from top to bottom.
        """
        #cache energy values to avoid redundant computation
        self.energy_cache = {}
        
        if dp:
            return self._best_seam_dp()
        else:
            return self._best_seam_naive()
    
    def _get_energy(self, i, j):
        """Get energy with caching."""
        if (i, j) not in self.energy_cache:
            self.energy_cache[i, j] = self.energy(i, j)
        return self.energy_cache[i, j]
    
    def _best_seam_dp(self):
        """Dynamic programming approach to find the best seam."""
        #create DP table: dp[i][j] = minimum energy to reach pixel (i, j) from top
        dp = {}
        parent = {} #to reconstruct the seam path
        
        #base case: first row
        for i in range(self.width):
            dp[i, 0] = self._get_energy(i, 0)
            parent[i, 0] = None
        
        #fill the DP table row by row
        for j in range(1, self.height):
            for i in range(self.width):
                #find minimum energy from previous row
                min_energy = float('inf')
                best_prev_i = None
                
                #check three possible previous positions
                for prev_i in [i-1, i, i+1]:
                    if 0 <= prev_i < self.width:
                        prev_energy = dp[prev_i, j-1]
                        if prev_energy < min_energy:
                            min_energy = prev_energy
                            best_prev_i = prev_i
                
                dp[i, j] = min_energy + self._get_energy(i, j)
                parent[i, j] = best_prev_i
        
        #find the minimum energy endpoint in the bottom row
        min_energy = float('inf')
        best_i = None
        for i in range(self.width):
            if dp[i, self.height - 1] < min_energy:
                min_energy = dp[i, self.height - 1]
                best_i = i
        
        #reconstruct the seam by backtracking
        seam = []
        i = best_i
        for j in range(self.height - 1, -1, -1):
            seam.append((i, j))
            if parent[i, j] is not None:
                i = parent[i, j]
        
        seam.reverse()
        return seam
    
    def _best_seam_naive(self):
        """Naive recursive approach to find the best seam."""
        #try all possible starting positions in the top row
        best_seam = None
        best_energy = float('inf')
        energy_memo = {}
        for i in range(self.width):
            seam, energy = self._compute_seam_from(i, 0)
            if energy < best_energy:
                best_energy = energy
                best_seam = seam
        
        return best_seam
    
    def _compute_seam_from(self, i, j):
        """Recursively compute the best seam starting from pixel (i, j).
        
        Returns:
            Tuple of (seam, total_energy) where seam is a list of coordinates.
        """
        current_energy = self._get_energy(i, j)
        
        #base case: last row
        if j == self.height - 1:
            return [(i, j)], current_energy
        
        #recursive case: try all valid next positions
        best_seam = None
        best_energy = float('inf')
        
        for next_i in [i-1, i, i+1]:
            if 0 <= next_i < self.width:
                seam, energy = self._compute_seam_from(next_i, j + 1)
                if energy < best_energy:
                    best_energy = energy
                    best_seam = seam
        
        #prepend current position to the best continuation
        return [(i, j)] + best_seam, current_energy + best_energy

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())