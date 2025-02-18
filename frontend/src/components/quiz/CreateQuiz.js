import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Formik, Form } from 'formik';
import * as Yup from 'yup';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
} from '@mui/material';
import { quizzes } from '../../services/api';

const validationSchema = Yup.object({
  title: Yup.string().required('Title is required'),
  total_questions: Yup.number()
    .required('Total questions is required')
    .min(1, 'Must have at least 1 question'),
  total_score: Yup.number()
    .required('Total score is required')
    .min(1, 'Total score must be at least 1'),
  duration: Yup.number()
    .required('Duration is required')
    .min(1, 'Duration must be at least 1 minute'),
});

function CreateQuiz() {
  const navigate = useNavigate();
  const [error, setError] = useState('');

  const handleSubmit = async (values) => {
    try {
      const quizData = {
        title: values.title.trim(),
        total_questions: parseInt(values.total_questions),
        total_score: parseInt(values.total_score),
        duration: parseInt(values.duration),
      };

      const response = await quizzes.createQuiz(quizData);
      if (response?.data?.id) {
        navigate('/dashboard');
      } else {
        setError('Failed to create quiz. Please try again.');
      }
    } catch (err) {
      console.error('Quiz creation error:', err);
      setError(err.response?.data?.detail || 'Failed to create quiz. Please try again.');
    }
  };

  return (
    <Container maxWidth="md">
      <Box my={4}>
        {error && (
          <Alert severity="error" sx={{ marginBottom: 2 }}>
            {error}
          </Alert>
        )}
        <Paper elevation={3}>
          <Box p={4}>
            <Typography variant="h4" gutterBottom>
              Create New Quiz
            </Typography>

            <Formik
              initialValues={{
                title: '',
                total_questions: '',
                total_score: '',
                duration: '',
              }}
              validationSchema={validationSchema}
              onSubmit={handleSubmit}
            >
              {({ values, errors, touched, handleChange, handleBlur, isSubmitting }) => (
                <Form>
                  <TextField
                    fullWidth
                    margin="normal"
                    name="title"
                    label="Quiz Title"
                    value={values.title}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={touched.title && Boolean(errors.title)}
                    helperText={touched.title && errors.title}
                  />
                  
                  <TextField
                    fullWidth
                    margin="normal"
                    name="total_questions"
                    label="Total Questions"
                    type="number"
                    value={values.total_questions}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={touched.total_questions && Boolean(errors.total_questions)}
                    helperText={touched.total_questions && errors.total_questions}
                  />

                  <TextField
                    fullWidth
                    margin="normal"
                    name="total_score"
                    label="Total Score"
                    type="number"
                    value={values.total_score}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={touched.total_score && Boolean(errors.total_score)}
                    helperText={touched.total_score && errors.total_score}
                  />

                  <TextField
                    fullWidth
                    margin="normal"
                    name="duration"
                    label="Duration (minutes)"
                    type="number"
                    value={values.duration}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    error={touched.duration && Boolean(errors.duration)}
                    helperText={touched.duration && errors.duration}
                  />

                  <Box mt={3} display="flex" justifyContent="flex-end">
                    <Button
                      variant="contained"
                      color="primary"
                      type="submit"
                      disabled={isSubmitting}
                    >
                      Create Quiz
                    </Button>
                  </Box>
                </Form>
              )}
            </Formik>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}

export default CreateQuiz;