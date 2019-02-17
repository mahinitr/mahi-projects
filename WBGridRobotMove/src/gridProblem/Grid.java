package gridProblem;

enum Color{
	BLACK,
	WHITE;
}

class Cell{
	Color color;
	
	Cell(Color color){
		this.color = color;
	}
	
	void flipColor() {
		if(color == Color.BLACK) {
			color = Color.WHITE;
		}else {
			color = Color.BLACK;
		}
	}
	
}

class Position{
	int x,y;
	Position(int x, int y){
		this.x = x;
		this.y = y;
	}
	
	Position getNextPos(Direction dir) {
		Position new_pos = new Position(x,y);
		if(dir.dir == Direction.ZERO) {
			new_pos.x = new_pos.x - 1;
		}
		else if(dir.dir == Direction.TWO) {
			new_pos.x = new_pos.x + 1;
		}
		else if(dir.dir == Direction.ONE) {
			new_pos.y = new_pos.y + 1;
		}
		else if(dir.dir == Direction.THREE) {
			new_pos.y = new_pos.y - 1;
		}
		return new_pos;
	}
}

public class Grid {
	
	int m,n;
	Cell[][] grid;
	

	public Grid(int m, int n) {
		this.m = m;
		this.n = n;
		grid = new Cell[m][n];
	}
	
	Cell getCell(Position pos) {
		if(pos.x >=0 && pos.x < m) {
			if(pos.y >=0 && pos.y < n) {
				return grid[pos.x][pos.y];
			}
		}
		return null;
	}
	
	void initializeGrid(Color[] colors, Robot robot) {
		if(colors.length < m * n) {
			System.out.println("Less no of input colors for grid");
			return;
		}
		
		int k = 0;
		for(int i = 0; i < m; i++) {
			for(int j=0; j < n; j++) {
				grid[i][j] = new Cell(colors[k]);
				k++;
			}
		}
		
		robot.grid = this;
	}
	
	boolean isMovePossible(Position pos) {
		if(pos.x >=0 && pos.x < m) {
			if(pos.y >=0 && pos.y < n) {
				return true;
			}
		}
		return false;
	}
	/*
	void applyDir() {
		Cell current_cell = getCell(robot.pos);
		Direction new_dir = null;
		if(current_cell.color == Color.WHITE) {
			new_dir = robot.dir.getRightDir();
		}else {
			new_dir = robot.dir.getLeftDir();
		}
		Position new_pos = robot.pos.getNextPos(new_dir);
		if(this.isMovePossible(new_pos)) {
			current_cell.flipColor();
			robot.setPos(new_pos);
		}
		robot.setDir(new_dir);
	}
	*/
	void printGrid() {
		for(int i=0; i<m; i++) {
			for(int j=0; j<n; j++) {
				Cell cell = grid[i][j];
				System.out.print(cell.color + "        ");
			}
			System.out.println();
		}
	}
	

}
