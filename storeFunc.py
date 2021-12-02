import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

class functions:
    def __init__(self, n_row, n_col, probInitBacteria, diffusionRate, probGrow, consumeRate, iter):
        self.n_row = n_row
        self.n_col = n_col
        self.probInitBacteria = probInitBacteria
        self.diffusionRate = diffusionRate
        self.probGrow = probGrow
        self.consumeRate = consumeRate
        self.iter = iter

    def _generate_matrix(self, n_row, n_col, probInitBacteria):
        """ Creates the base matrix for the nutrition and bacteria 
            and also the coordinates and the nutrition of the bacteria
        
        :param n_row: the number of rows of the matrix
        :param n_col: the number of columns of the matrix
        :param probInitBacteria: the probability of a bacteria to spawn in the cells
        :return mat_nutrition: matrix containing the nutrition for the bacteria ranging from 0 to 10
        :return mat_bacteria: matrix containing the bacteria with 1 indicates a bacteria and 2 indicates dead bacteria
        :return bacteria: list containing a lists of the bacteria's coordinate on 1st index and its nutrition level on the 2nd index

        """
        mat_nutrition = np.array([np.array([float(10) for _ in range(n_col)]) for _ in range(n_row)])
        mat_bacteria = np.zeros((n_row, n_col))
        bacterias = []
        for i in range(0, n_row):
            rand = np.random.rand(1)
            if rand < probInitBacteria:
                mat_bacteria[i, 0] =  1
                bacterias.append([[i, 0], 10])
        self.mat_nutrition = mat_nutrition
        self.mat_bacteria = mat_bacteria
        self.bacterias = bacterias
        return (self.mat_nutrition, self.mat_bacteria, self.bacterias)

    def _nutrition_diffusion(self, mat_nutrition, diffusionRate):
        """ Diffuse the nutrition matrix according to its diffusion rate

        :param mat_nutrition: the nutrition matrix
        :param diffusionRate: the rate of nutrition diffusion
        :return mat_nutrition: the diffuted nutrition matrix
        """
        for i in range(0, mat_nutrition.shape[1]):
            if np.all(mat_nutrition[:, i] == 10):
                break
        for col in range(0, i+1):
            for row in range(0, mat_nutrition.shape[0]):
                if mat_nutrition[row, col] - diffusionRate > 0:
                    mat_nutrition[row, col] = mat_nutrition[row, col] - diffusionRate
                else:
                    mat_nutrition[row, col] = 0
        self.mat_nutrition = mat_nutrition
        return self.mat_nutrition
    
    def _find_neighbors_coordinates(self, coor_x, coor_y, mat_bacteria):
        """ Find the bacteria's neighbor's coordinate

        :param coor_x: the x axis coordinate of the bacteria
        :param coor_y: the y axis coordinate of the bacteria
        :param mat_bacteria: the bacteria's matrix
        :return neighbors: all of the bacteria's neighbor's coordinate
        """
        top = [coor_x-1, coor_y]
        right = [coor_x, coor_y+1]
        bottom = [coor_x+1, coor_y]
        left = [coor_x, coor_y-1]
        temp_neighbors = [top, right, bottom, left]
        neighbors = []
        for neighbor in temp_neighbors:
            if neighbor[0] >= 0 and neighbor[0] < mat_bacteria.shape[0]:
                if neighbor[1] >= 0 and neighbor[1] < mat_bacteria.shape[1]:
                    if mat_bacteria[neighbor[0], neighbor[1]] == 0:
                        neighbors.append(neighbor)
        self.neighbors = neighbors
        return self.neighbors

    def _bacterial_food_consumptions(self, mat_bacteria, bacterias, consumeRate):
        """ Reduce the bacteria's nutrition by its consume rate

        :param mat_bacteria: matrix containing bacterias
        :param bacterias: list containing lists of bacteria's coordinate and nutrition level
        :param consumeRate: the bacteri's food consumption rate
        """
        temp_bacterias = []
        for bacteria in bacterias:
            bacteria_coor = bacteria[0]
            bacteria_nutrition = bacteria[1]
            if bacteria_nutrition - consumeRate >= 0:
                remain_nutrition = bacteria_nutrition - consumeRate
                temp_bacterias.append([bacteria_coor, remain_nutrition])
            else:
                mat_bacteria[bacteria_coor[0], bacteria_coor[1]] = 2
        self.mat_bacteria = mat_bacteria
        self.bacterias = temp_bacterias
        return (self.mat_bacteria, self.bacterias)
    
    def _bacterial_grow(self, probGrow, mat_bacteria, mat_nutrition, nutritionLevel, neighbors, bacterias):
        """ Spawns the bacteria in its available neighbor
        :param probGrow: the probabilty inverse for the bacterial grow probability
        :param mat_bacteria: matrix containing bacterias
        :param mat_nutrition: matrix containing nutritions
        :param nutritionLevel: the bacteria's nutrition level
        :param neighbors: the bacteria's neighbor coordinates
        :param nutritionLevel: the bacteria's nutrition level
        :param bacterias: list containing lists of bacteria's coordinate and nutrition level
        :return mat_bacteria: matrix containing the previous and the newly grown bacterias
        :return bacterias: list containing lists of bacteria's coordinate and nutrition level for the previous and newly grown bacterias
        """
        growProb = nutritionLevel / probGrow
        for neighbor in neighbors:
            rand = np.random.rand(1)
            if rand < growProb:
                mat_bacteria[neighbor[0], neighbor[1]] = 1
                neighbor_nutrition =  mat_nutrition[neighbor[0], neighbor[1]]
                bacterias.append([neighbor, neighbor_nutrition])
        self.mat_bacteria = mat_bacteria
        self.bacterias = bacterias
        return (self.mat_bacteria, self.bacterias)
            
    def _update_nutrion_matrix(self, mat_bacteria, mat_nutrition):
        """ Updates the nutrition matrix to according to its bacteria's matrix

        :param mat_bacteria: matrix containing bacterias
        :param mat_nutrition: matrix containing nutritions
        :return mat_nutrition: the updated nutrition matrix
        """
        for r, row in enumerate(mat_bacteria):
            for c, cell in enumerate(row):
                if cell != 0:
                    mat_nutrition[r, c] = 0
        self.mat_nutrition = mat_nutrition
        return self.mat_nutrition
    
    def simulate(self):
        bacteria_frames = np.zeros((self.iter, self.n_row, self.n_col))
        nutrition_frames = np.zeros((self.iter, self.n_row, self.n_col))

        self._generate_matrix(self.n_row, self.n_col, self.probInitBacteria)
        bacteria_frames[0] = self.mat_bacteria
        nutrition_frames[0] = self.mat_nutrition
        for i in range(1, self.iter):
            for bacteria in self.bacterias:
                nutritionLevel = bacteria[1]
                coor_x = bacteria[0][0]
                coor_y = bacteria[0][1]
                self._find_neighbors_coordinates(coor_x, coor_y, self.mat_bacteria)
                self._bacterial_grow(self.probGrow, self.mat_bacteria, self.mat_nutrition, nutritionLevel, self.neighbors, self.bacterias)
            self._bacterial_food_consumptions(self.mat_bacteria, self.bacterias, self.consumeRate)
            self._update_nutrion_matrix(self.mat_bacteria, self.mat_nutrition)
            self._nutrition_diffusion(self.mat_nutrition, self.diffusionRate)
            bacteria_frames[i] = self.mat_bacteria
            nutrition_frames[i] = self.mat_nutrition
        return (bacteria_frames, nutrition_frames)






        


    

            




        




        
