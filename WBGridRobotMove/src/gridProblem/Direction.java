
package gridProblem;

public class Direction {
	
	// possible directions are 0, 1, 2, 3
	static final int ZERO = 0;
	static final int ONE = 1;
	static final int TWO = 2;
	static final int THREE = 3;
	
	static final int MAX_DIR_BOUND = 4;
	int dir;
	
	static int bounded_value(int d) {
		return d % MAX_DIR_BOUND;
	}

	public Direction(int d) {
		if(d < 0) {
			d = Direction.THREE;
		}
		this.dir = Direction.bounded_value(d);
	}
	
	Direction getLeftDir() {
		int new_dir = this.dir - 1;
		return new Direction(new_dir);
	}
	
	Direction getRightDir() {
		int new_dir = this.dir + 1;
		if(new_dir < 0) {
			new_dir = Direction.THREE;
		}
		return new Direction(new_dir);
	}

}
