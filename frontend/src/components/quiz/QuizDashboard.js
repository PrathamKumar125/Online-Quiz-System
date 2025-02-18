import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { quizzes } from '../../services/api';
import {
  Container,
  Grid,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  Button,
  Box,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import api from '../../services/api';

function QuizDashboard() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [quizList, setQuizList] = useState([]);
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [userScores, setUserScores] = useState([]);

  useEffect(() => {
    fetchQuizzes();
  }, []);

  const fetchQuizzes = async () => {
    try {
      const response = await api.quizzes.getUserQuizzes();
      const userQuizzes = Array.isArray(response.data) ? response.data : [];
      setQuizList(userQuizzes);
      if (userQuizzes.length > 0) {
        setSelectedQuiz(userQuizzes[0]);
        const scoresResponse = await api.quizzes.getQuizScores(userQuizzes[0].id);
        setUserScores(Array.isArray(scoresResponse.data) ? scoresResponse.data : []);
      }
    } catch (err) {
      console.error('Error fetching quizzes:', err.response || err);
      setError(`Failed to load quizzes: ${err.response?.data?.detail || err.message || 'Please try again later.'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleQuizSelect = async (quiz) => {
    setSelectedQuiz(quiz);
    try {
      const scoresResponse = await quizzes.getQuizScores(quiz.id);
      setUserScores(Array.isArray(scoresResponse.data) ? scoresResponse.data : []);
    } catch (err) {
      console.error('Error fetching scores:', err);
      setUserScores([]);
    }
  };

  if (error) {
    return (
      <Container maxWidth="lg">
        <Box my={4}>
          <Alert severity="error">{error}</Alert>
        </Box>
      </Container>
    );
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box my={4}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Paper elevation={3}>
              <Box p={2} display="flex" justifyContent="space-between" alignItems="center">
                <Typography variant="h6">Quizzes</Typography>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<AddIcon />}
                  onClick={() => navigate('/create-quiz')}
                >
                  Create Quiz
                </Button>
              </Box>
              <List>
                {quizList.map((quiz) => (
                  <ListItem
                    button
                    key={quiz.id}
                    selected={selectedQuiz?.id === quiz.id}
                    onClick={() => handleQuizSelect(quiz)}
                  >
                    <ListItemText
                      primary={quiz.title}
                      secondary={`Questions: ${quiz.total_questions} | Score: ${quiz.total_score}`}
                    />
                  </ListItem>
                ))}
                {quizList.length === 0 && (
                  <ListItem>
                    <ListItemText primary="No quizzes available" />
                  </ListItem>
                )}
              </List>
            </Paper>
          </Grid>

          <Grid item xs={12} md={8}>
            {selectedQuiz ? (
              <Paper elevation={3}>
                <Box p={3}>
                  <Typography variant="h5" gutterBottom>
                    {selectedQuiz.title}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    Duration: {selectedQuiz.duration} minutes | Total Questions: {selectedQuiz.total_questions}
                  </Typography>
                  <Box my={3}>
                    <Typography variant="h6" gutterBottom>
                      Recent Attempts
                    </Typography>
                    <TableContainer>
                      <Table>
                        <TableHead>
                          <TableRow>
                            <TableCell>User</TableCell>
                            <TableCell align="right">Score</TableCell>
                            <TableCell align="right">Date</TableCell>
                            <TableCell align="right">Actions</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {userScores.map((score, index) => (
                            <TableRow key={`score-${score.id || index}`}>
                              <TableCell component="th" scope="row">
                                {score.username}
                              </TableCell>
                              <TableCell align="right">
                                {score.score}/{selectedQuiz.total_score}
                              </TableCell>
                              <TableCell align="right">
                                {new Date(score.completed_at).toLocaleDateString()}
                              </TableCell>
                              <TableCell align="right">
                                <Button
                                  size="small"
                                  color="primary"
                                  onClick={() => navigate(`/score/${score.id}`)}
                                >
                                  View Details
                                </Button>
                              </TableCell>
                            </TableRow>
                          ))}
                          {userScores.length === 0 && (
                            <TableRow key="no-scores">
                              <TableCell colSpan={4} align="center">
                                No attempts yet
                              </TableCell>
                            </TableRow>
                          )}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </Box>
                  <Box display="flex" justifyContent="flex-end" mt={2}>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => navigate(`/quiz/${selectedQuiz.id}`)}
                    >
                      Start Quiz
                    </Button>
                  </Box>
                </Box>
              </Paper>
            ) : (
              <Paper elevation={3}>
                <Box p={3} textAlign="center">
                  <Typography variant="h6" color="textSecondary">
                    Select a quiz to view details
                  </Typography>
                </Box>
              </Paper>
            )}
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
}

export default QuizDashboard;