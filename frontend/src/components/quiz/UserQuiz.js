import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  Button,
  Box,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Alert,
} from '@mui/material';
import { quizzes } from '../../services/api';

function UserQuiz() {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const mountedRef = useRef(false);
  const [quiz, setQuiz] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [confirmSubmit, setConfirmSubmit] = useState(false);

  const handleSubmit = useCallback(async () => {
    if (!quiz || !quizId) return;
    try {
      await quizzes.submitQuizAttempt(quizId, {
        attempt_id: localStorage.getItem(`quiz_attempt_${quizId}`),
        responses: Object.entries(answers).map(([questionId, optionId]) => ({
          question_id: parseInt(questionId),
          selected_option_id: parseInt(optionId)
        }))
      });
      navigate(`/score/${quizId}`);
    } catch (err) {
      setError('Failed to submit quiz. Please try again.');
    }
  }, [quizId, answers, navigate, quiz]);

  const fetchQuizData = useCallback(async () => {
    try {
        setLoading(true);
        setError('');
        console.log('Fetching quiz data for ID:', quizId);
        
        if (!quizId) {
            throw new Error('Quiz ID is required');
        }

        // First get the quiz data
        const quizResponse = await quizzes.get(quizId);
        console.log('Quiz data received:', quizResponse.data);
        
        if (!quizResponse.data || !quizResponse.data.questions || quizResponse.data.questions.length === 0) {
            throw new Error('Invalid quiz data received');
        }

        // Start the quiz attempt only if we have valid quiz data
        const startResponse = await quizzes.startQuizAttempt(quizId);
        console.log('Quiz attempt started:', startResponse.data);
        
        if (!startResponse.data || !startResponse.data.attempt_id) {
            throw new Error('Failed to start quiz attempt');
        }
        
        setQuiz(quizResponse.data);
        setTimeLeft(quizResponse.data.duration * 60);
        localStorage.setItem(`quiz_attempt_${quizId}`, startResponse.data.attempt_id);
    } catch (err) {
        console.error('Error fetching quiz:', err);
        const errorMessage = err.response?.data?.detail || 
                           err.response?.statusText ||
                           err.message || 
                           'Failed to load quiz. Please try again.';
        setError(errorMessage);
    } finally {
        setLoading(false);
    }
}, [quizId]);

  useEffect(() => {
    let isMounted = true;
    
    if (isMounted && !quiz) {
      fetchQuizData();
    }
    
    return () => {
      isMounted = false;
    };
  }, [fetchQuizData, quiz]);

  useEffect(() => {
    if (timeLeft === null) return;

    if (timeLeft === 0) {
      handleSubmit();
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, handleSubmit]);

  const handleAnswerSelect = (questionId, optionId) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: optionId,
    }));
  };

  if (loading) {
    return (
      <Container maxWidth="md">
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <CircularProgress />
          <Typography variant="h6" sx={{ ml: 2 }}>
            Loading quiz...
          </Typography>
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md">
        <Box my={4}>
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
          <Button variant="contained" color="primary" onClick={() => navigate('/dashboard')}>
            Return to Dashboard
          </Button>
        </Box>
      </Container>
    );
  }

  if (!quiz || !quiz.questions || quiz.questions.length === 0) {
    return (
      <Container maxWidth="md">
        <Box my={4}>
          <Alert severity="warning">
            No questions found for this quiz.
          </Alert>
          <Box mt={2}>
            <Button variant="contained" color="primary" onClick={() => navigate('/dashboard')}>
              Return to Dashboard
            </Button>
          </Box>
        </Box>
      </Container>
    );
  }

  const currentQuestion = quiz?.questions?.[currentQuestionIndex];
  if (!quiz || !currentQuestion) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Paper elevation={3}>
          <Box p={4}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
              <Typography variant="h4">{quiz?.title}</Typography>
              <Typography variant="h6" color="primary">
                Time Left: {formatTime(timeLeft)}
              </Typography>
            </Box>

            <LinearProgress
              variant="determinate"
              value={(currentQuestionIndex + 1) * (100 / quiz?.questions.length)}
              style={{ marginBottom: '2rem' }}
            />

            {currentQuestion && (
              <>
                <Typography variant="h6" gutterBottom>
                  Question {currentQuestionIndex + 1} of {quiz.questions.length}
                </Typography>
                <Typography variant="body1" paragraph>
                  {currentQuestion.text}
                </Typography>

                <FormControl component="fieldset">
                  <RadioGroup
                    value={answers[currentQuestion.id] || ''}
                    onChange={(e) => handleAnswerSelect(currentQuestion.id, e.target.value)}
                  >
                    {currentQuestion.options.map((option) => (
                      <FormControlLabel
                        key={option.id}
                        value={option.id.toString()}
                        control={<Radio />}
                        label={option.text}
                      />
                    ))}
                  </RadioGroup>
                </FormControl>
              </>
            )}

            <Box display="flex" justifyContent="space-between" mt={4}>
              <Button
                variant="outlined"
                disabled={currentQuestionIndex === 0}
                onClick={() => setCurrentQuestionIndex((prev) => prev - 1)}
              >
                Previous
              </Button>
              {currentQuestionIndex === quiz?.questions.length - 1 ? (
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => setConfirmSubmit(true)}
                  disabled={Object.keys(answers).length !== quiz?.questions.length}
                >
                  Submit Quiz
                </Button>
              ) : (
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => setCurrentQuestionIndex((prev) => prev + 1)}
                >
                  Next
                </Button>
              )}
            </Box>
          </Box>
        </Paper>
      </Box>

      <Dialog open={confirmSubmit} onClose={() => setConfirmSubmit(false)}>
        <DialogTitle>Submit Quiz</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to submit the quiz? You won't be able to change your answers after
            submission.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmSubmit(false)} color="primary">
            Cancel
          </Button>
          <Button onClick={handleSubmit} color="primary" variant="contained">
            Submit
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default UserQuiz;