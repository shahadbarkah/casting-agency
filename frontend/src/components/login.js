import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import {Button, Navbar, NavDropdown} from 'react-bootstrap'

function Login() {
  const {
    isLoading,
    isAuthenticated,
    error,
    user,
    loginWithRedirect,
    logout,
  } = useAuth0();

   if (isLoading) {
    return <Navbar.Text>Loading...</Navbar.Text>;
  }

  if (isAuthenticated) {
    return (
        <>
        <Navbar.Text>Hello</Navbar.Text>
         <NavDropdown title={user.name} id="collasible-nav-dropdown">
          <NavDropdown.Item onClick={() => logout({ returnTo: window.location.origin })}>Log out</NavDropdown.Item>
        </NavDropdown>
        
        </>
    
    );
  } else {  
    return <Button variant="light" size="sm" onClick={loginWithRedirect}> Login</Button>;
  }
}

export default Login;