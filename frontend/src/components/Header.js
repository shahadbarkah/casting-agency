import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import {Navbar, Nav, Container, Button} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.css';
import { useAuth0 } from '@auth0/auth0-react';
import Login from './login';
import '../App.css';
function Header() { 
    const {
    isLoading,
    isAuthenticated,
    error,
    user,
    loginWithRedirect,
    logout,
  } = useAuth0();

        return(
        <Navbar bg="dark" variant="dark" sticky='top'>
            <Container>
            <Navbar.Brand as={Link} to='/' >Casting Agency</Navbar.Brand>
            <Nav className="me-auto">
            <Nav.Link as={Link} to='/'>Home</Nav.Link>
            <Nav.Link as={Link} to='/actors'>Actors</Nav.Link>
            <Nav.Link as={Link} to='/movies'>Movies</Nav.Link>
            </Nav>
            <Nav className="ml-auto">
            <Login/>
            </Nav>
            </Container>
        </Navbar>
        
  
        );
    }

export default Header;