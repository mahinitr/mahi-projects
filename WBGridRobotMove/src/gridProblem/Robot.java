package gridProblem;

public class Robot {
	
	Position pos;
	Direction dir;
	Grid grid;

	public Robot(Position pos, Direction dir) {
		this.pos = pos;
		this.dir = dir;
	}

	public void setPos(Position pos) {
		this.pos = pos;
	}

	public void setDir(Direction dir) {
		this.dir = dir;
	}
	
	void moveDir() {
		Cell current_cell = grid.getCell(this.pos);
		Direction new_dir = null;
		if(current_cell.color == Color.WHITE) {
			new_dir = this.dir.getRightDir();
		}else {
			new_dir = this.dir.getLeftDir();
		}
		Position new_pos = this.pos.getNextPos(new_dir);
		if(grid.isMovePossible(new_pos)) {
			current_cell.flipColor();
			this.setPos(new_pos);
		}
		this.setDir(new_dir);
	}
	
}
