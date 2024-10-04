class Percolation:
    
    def __init__(self, n):
        self.n = n
        self.grid = [[False] * n for _ in range(n)]
        self.open_sites_count = 0
        self.parent = list(range(n * n + 1))
        self.rank = [0] * (n * n + 1)
        self.virtual_top = n * n

    def index(self, row, col):
        """Convert (row, col) to a single index."""
        return row * self.n + col

    def find(self, p):
        """Find the root of p with path compression."""
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])
        return self.parent[p]

    def union(self, p, q):
        """Union the sets containing p and q."""
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP != rootQ:
            # Union by rank
            if self.rank[rootP] > self.rank[rootQ]:
                self.parent[rootQ] = rootP
            elif self.rank[rootP] < self.rank[rootQ]:
                self.parent[rootP] = rootQ
            else:
                self.parent[rootQ] = rootP
                self.rank[rootP] += 1

    def open(self, row, col):
        """Open the site (row, col) if it is not open already."""
        if self.isOpen(row, col):
            return
        self.grid[row][col] = True
        self.open_sites_count += 1
        
        index = self.index(row, col)

        if row == 0:
            self.union(index, self.virtual_top)
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.n and 0 <= new_col < self.n and self.isOpen(new_row, new_col):
                self.union(index, self.index(new_row, new_col))
        
    def isOpen(self, row, col):
        """Is the site (row, col) open?"""
        return self.grid[row][col]

    def isFull(self, row, col):
        """Is the site (row, col) full?"""
        return self.connected(self.index(row, col), self.virtual_top)

    def numberOfOpenSites(self):
        """Return the number of open sites."""
        return self.open_sites_count

    def percolates(self):
        """Does the system percolate?"""
        for col in range(self.n):
            if self.isFull(self.n - 1, col):
                return True
        return False

    def connected(self, p, q):
        """Check if p and q are connected."""
        return self.find(p) == self.find(q)

    def get_grid(self):
        GREEN = "\033[32m"
        RESET = "\033[0m"
    
        for row in self.grid:
            colored_row = [
                f"{GREEN}True{RESET}" if site else f"False{RESET}" for site in row
            ]
            print(" ".join(colored_row))
        return self.grid