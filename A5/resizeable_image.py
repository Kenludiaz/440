import imagematrix
import sys

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp=False):
        self.naive_seam_carving()

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())

    def naive_pixel_traversal(self, coordinates, all_seams, energy = 0, path = []):
        
        energy += self.energy(coordinates[0], coordinates[1])
        path.append(coordinates)
        print(self[coordinates[0], coordinates[1]])
        if (coordinates[0] == self.height - 1):
            all_seams.append((energy, path))
            return

        if coordinates[1] > 0:
            left_down = [coordinates[0] + 1, coordinates[1] - 1]
            self.naive_pixel_traversal(left_down, all_seams, energy, path.copy() )

        down = [coordinates[0] + 1, coordinates[1]]
        self.naive_pixel_traversal(down, all_seams, energy, path.copy() )

        right_down = [coordinates[0] + 1, coordinates[1] + 1]
        self.naive_pixel_traversal(right_down, all_seams, energy, path.copy() )

    def naive_seam_carving(self):
        all_seams = []
        for col in range(self.width):
            self.naive_pixel_traversal([0, col], all_seams)
        min = 100000
        min_index = 0
        for seam in all_seams:
            if seam[0] < min:
                min = seam[0]
                min_index = all_seams.index(seam)
        return all_seams[min_index][1]
        
