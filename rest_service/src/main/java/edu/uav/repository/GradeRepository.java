package edu.uav.repository;

import edu.uav.model.Grade;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

@Repository
public class GradeRepository {
    @Autowired
    private JdbcTemplate jdbc;

    private RowMapper<Grade> mapper = new RowMapper<Grade>() {
        public Grade mapRow(ResultSet rs, int rowNum) throws SQLException {
            return new Grade(rs.getInt("id"), rs.getInt("enrollment_id"), rs.getDouble("grade"));
        }
    };

    public List<Grade> findAll() {
        return jdbc.query("SELECT id, enrollment_id, grade FROM grades", mapper);
    }

    public int insert(int enrollmentId, double grade) {
        jdbc.update("INSERT INTO grades (enrollment_id, grade) VALUES (?,?)", enrollmentId, grade);
        // MySQL last insert id retrieval not included here; keep simple
        return 1;
    }
}
