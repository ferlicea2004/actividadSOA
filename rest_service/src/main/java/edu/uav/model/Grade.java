package edu.uav.model;

public class Grade {
    private int id;
    private int enrollmentId;
    private double grade;

    public Grade() {}

    public Grade(int id, int enrollmentId, double grade) {
        this.id = id;
        this.enrollmentId = enrollmentId;
        this.grade = grade;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }

    public int getEnrollmentId() { return enrollmentId; }
    public void setEnrollmentId(int enrollmentId) { this.enrollmentId = enrollmentId; }

    public double getGrade() { return grade; }
    public void setGrade(double grade) { this.grade = grade; }
}
