using System.Collections.Generic;
using System.Linq;

namespace Dungeon;

public class BfsTask
{
	public static IEnumerable<SinglyLinkedList<Point>> FindPaths(Map map, Point start, Point[] chests)
	{
		if (chests.Length == 0) yield break;

		var queue = new Queue<SinglyLinkedList<Point>>();
		queue.Enqueue(new SinglyLinkedList<Point>(start));
		var visitedPoints = new HashSet<Point>();
		var chestsLeft = new HashSet<Point>(chests);
		var possibleDirections = Walker.PossibleDirections;

		while (queue.Count != 0)
		{
			var currentPoint = queue.Dequeue();

			if (chestsLeft.Contains(currentPoint.Value))
			{
				yield return currentPoint;
				chestsLeft.Remove(currentPoint.Value);
				if (chestsLeft.Count == 0) yield break;
			}

			foreach (var direction in possibleDirections)
			{
				AddExistingNode(map, currentPoint, direction, visitedPoints, queue);
			}
		}
		
	}

	private static void AddExistingNode(Map map, SinglyLinkedList<Point> currentPoint, Point direction,
		HashSet<Point> visitedPoints,
		Queue<SinglyLinkedList<Point>> queue)
	{
		var newPoint = currentPoint.Value + direction;
		if (visitedPoints.Contains(newPoint)) return;
		if (map.InBounds(newPoint) && (map.Dungeon[newPoint.X, newPoint.Y] == MapCell.Empty))
		{
			queue.Enqueue(new SinglyLinkedList<Point>(newPoint, currentPoint));
			visitedPoints.Add(newPoint);
		}
	}
}