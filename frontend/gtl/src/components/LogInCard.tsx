import React, { useEffect, useState } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Box from '@material-ui/core/Box';

import IPerson from '../types/Person';
import PersonService from '../services/PersonService';

const LogInCard: React.FC = () => {
  const [persons, setPersons] = useState<Array<IPerson>>([])
  const [fetchIsDone, setFetchIsDone] = useState(false)

  useEffect(() => {
    retrievePersons()
  }, [])

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const email = data.get('email')
    const password = data.get('password')
    console.log("Submitted: ", email, password);
    for(const key in persons){
      const person = persons[key]
      if (person.email === email && person.password === password){
        console.log("Success!")
      }
    }
  };

  const retrievePersons = () => {
    PersonService.getAll()
      .then((response: any) => {
        setPersons(response.data.items)
        setFetchIsDone(true)
      })
      .catch((e: Error) => {
        console.log(e)
      })
  }
  return (
    <Box component="form" onSubmit={handleSubmit} >
      <TextField
        margin="normal"
        required
        fullWidth
        id="email"
        label="Email Address"
        name="email"
        autoComplete="email"
        autoFocus
      />
      <TextField
        margin="normal"
        required
        fullWidth
        name="password"
        label="Password"
        type="password"
        id="password"
        autoComplete="current-password"
      />
      <Button type="submit" variant="outlined" >
        Log In
      </Button>
    </Box>
  );
}
export default LogInCard;