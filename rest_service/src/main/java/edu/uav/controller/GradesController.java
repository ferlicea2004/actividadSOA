package edu.uav.controller;

import edu.uav.model.Grade;
import edu.uav.repository.GradeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/grades")
public class GradesController {
    @Autowired
    private GradeRepository repo;

    @GetMapping
    public ResponseEntity<List<Grade>> list() {
        return ResponseEntity.ok(repo.findAll());
    }

    @PostMapping
    public ResponseEntity<String> create(@RequestParam int enrollmentId, @RequestParam double grade) {
        repo.insert(enrollmentId, grade);
        return ResponseEntity.ok("created");
    }
}
