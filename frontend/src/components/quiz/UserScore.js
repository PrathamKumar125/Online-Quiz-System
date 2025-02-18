import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
  Alert,
} from '@mui/material';
import { Check as CheckIcon, Close as CloseIcon } from '@mui/icons-material';
import { green, red } from '@mui/material/colors';
import { quizzes } from '../../services/api';

function UserScore() {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const [quizResponse, setQuizResponse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchQuizResponse = async () => {
      try {
        const response = await quizzes.getResponse(quizId);
        setQuizResponse(response.data);
      } catch (err) {
        setError('Failed to load quiz results. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchQuizResponse();
  }, [quizId]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md">
        <Box my={4}>
          <Alert severity="error">{error}</Alert>
          <Box mt={2}>
            <Button variant="contained" color="primary" onClick={() => navigate('/dashboard')}>
              Return to Dashboard
            </Button>
          </Box>
        </Box>
      </Container>
    );
  }

  const calculatePercentage = () => {
    const score = quizResponse.score;
    const total = quizResponse.total_score;
    return Math.round((score / total) * 100);
  };

  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Paper elevation={3}>
          <Box p={4}>
            <Typography variant="h4" gutterBottom>
              Quiz Results
            </Typography>

            <Box
              display="flex"
              flexDirection="column"
              alignItems="center"
              my={4}
              p={3}
              bgcolor="#f5f5f5"
              borderRadius={4}
            >
              <Typography variant="h3" color="primary" gutterBottom>
                {calculatePercentage()}%
              </Typography>
              <Typography variant="h6">
                Score: {quizResponse.score} / {quizResponse.total_score}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Completed on: {new Date(quizResponse.completed_at).toLocaleString()}
              </Typography>
            </Box>

            <Typography variant="h6" gutterBottom>
              Review Questions
            </Typography>

            <List>
              {quizResponse.questions.map((question, index) => (
                <React.Fragment key={question.id}>
                  <ListItem alignItems="flex-start">
                    <Box width="100%">
                      <Typography variant="subtitle1" gutterBottom>
                        Question {index + 1}: {question.text}
                      </Typography>

                      {question.options.map((option) => (
                        <Box
                          key={option.id}
                          display="flex"
                          alignItems="center"
                          mb={1}
                          p={1}
                          bgcolor={
                            option.is_correct
                              ? green[50]
                              : option.id === question.selected_option_id && !option.is_correct
                              ? red[50]
                              : 'transparent'
                          }
                          borderRadius={1}
                        >
                          {option.is_correct ? (
                            <CheckIcon style={{ color: green[500], marginRight: 8 }} />
                          ) : option.id === question.selected_option_id && !option.is_correct ? (
                            <CloseIcon style={{ color: red[500], marginRight: 8 }} />
                          ) : (
                            <Box width={32} />
                          )}
                          <ListItemText primary={option.text} />
                        </Box>
                      ))}

                      {question.explanation && (
                        <Box mt={1} p={2} bgcolor="#f8f8f8" borderRadius={1}>
                          <Typography variant="body2" color="textSecondary">
                            Explanation: {question.explanation}
                          </Typography>
                        </Box>
                      )}
                    </Box>
                  </ListItem>
                  {index < quizResponse.questions.length - 1 && <Divider component="li" />}
                </React.Fragment>
              ))}
            </List>

            <Box display="flex" justifyContent="space-between" mt={4}>
              <Button variant="outlined" onClick={() => navigate('/dashboard')}>
                Return to Dashboard
              </Button>
              <Button
                variant="contained"
                color="primary"
                onClick={() => navigate(`/quiz/${quizId}`)}
              >
                Retake Quiz
              </Button>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}

export default UserScore;