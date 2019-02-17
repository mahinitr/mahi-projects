package gridProblem;

public class TestGridProblem {

	public TestGridProblem() {
		// TODO Auto-generated constructor stub
	}
	
	static Grid grid;
	static Robot robot;

	public static void main(String[] args) {
		int m = 4;
		int n = 4;
		String[] grid_input =  {"W", "B","W", "B", "B", "W", "W", "B", "W","W", "B", "B", "W", "W", "B", "W"};
		int robot_x = 0, robot_y = 0;
		int robot_dir = Direction.ONE;
		int k = 6;
		
		
		Color[] grid_array = new Color[m*n];
		for(int i=0; i<m*n; i++) {
			if(grid_input[i] == "W")
				grid_array[i] = Color.WHITE;
			else
				grid_array[i] = Color.BLACK;
		}
		
		robot = new Robot(new Position(robot_x, robot_y), new Direction(robot_dir));
		
		TestGridProblem.grid = new Grid(m,n);
		TestGridProblem.grid.initializeGrid(grid_array, robot);
		System.out.println("Before  applying moves \n");
		TestGridProblem.grid.printGrid();
		printKMoves(k);
		System.out.println("\nAfter applying moves \n");
		TestGridProblem.grid.printGrid();
		
		
	}
	
	static void printKMoves(int k) {
		for(int i=0; i<k; i++) {
			System.out.println("move - " + (i+1));
			System.out.println("robot pos - " + robot.pos.x + "," + robot.pos.y);
			System.out.println("robot dir - " + robot.dir.dir);
			TestGridProblem.robot.moveDir();
			TestGridProblem.grid.printGrid();
		}
	}
}
