import java.util.*;

class Task {
    String name;
    int executionTime;
    int priority;
    double energyConsumption;

    public Task(String name, int executionTime, int priority) {
        this.name = name;
        this.executionTime = executionTime;
        this.priority = priority;
        this.energyConsumption = 0;
    }
}

class EnergyEfficientScheduler {
    private PriorityQueue<Task> taskQueue;
    private double cpuFrequency; // GHz
    private double basePower = 50; // Base power in Watts

    public EnergyEfficientScheduler() {
        this.taskQueue = new PriorityQueue<>(Comparator.comparingInt(t -> -t.priority));
        this.cpuFrequency = 2.5; // Default frequency in GHz
    }

    public void addTask(Task task) {
        taskQueue.add(task);
    }

    private double calculateEnergy(Task task) {
        return basePower * (task.executionTime / cpuFrequency);
    }

    public void executeTasks() {
        System.out.println("Executing Tasks with Energy-Efficient Scheduling...");
        while (!taskQueue.isEmpty()) {
            Task task = taskQueue.poll();
            adjustCpuFrequency(task);
            task.energyConsumption = calculateEnergy(task);
            System.out.println("Executing " + task.name + " | Priority: " + task.priority + " | Execution Time: "
                    + task.executionTime + " ms | Energy Used: " + String.format("%.2f", task.energyConsumption) + " J");
        }
    }

    private void adjustCpuFrequency(Task task) {
        if (task.priority > 7) {
            cpuFrequency = 3.5; // High priority -> Increase frequency
        } else if (task.priority > 4) {
            cpuFrequency = 2.5; // Medium priorjity -> Moderate frequency
        } else {
            cpuFrequency = 1.5; // Low priority -> Lower frequency to save energy
        }
        System.out.println("CPU Frequency adjusted to: " + cpuFrequency + " GHz");
    }
}

public class EnergyEfficientCPUScheduler {
    public static void main(String[] args) {
        EnergyEfficientScheduler scheduler = new EnergyEfficientScheduler();

        scheduler.addTask(new Task("Task 1", 100, 8));
        scheduler.addTask(new Task("Task 2", 150, 5));
        scheduler.addTask(new Task("Task 3", 200, 3));
        scheduler.addTask(new Task("Task 4", 120, 10));
        scheduler.addTask(new Task("Task 5", 80, 6));

        scheduler.executeTasks();
    }
}
