import React, { useState } from 'react';
import CameraComponent from './Components/CameraComponent';
import MessageDisplay from './Components/MessageDisplay';
import { Navbar, Container, Row, Col} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const App = () => {
    const [message, setMessage] = useState('');

    const handleValidation = (imageData) => {
        fetch('/reconocimiento_facial', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ imagen: imageData })
        })
        .then(response => response.text()) 
        .then(data => {
            setMessage(data);
        })
        .catch(error => {
            console.error('Error:', error);
            setMessage('Error al realizar la validación');
        });
    };

    return (
        <div className="d-flex flex-column" style={{ height: '100vh' }}>
            <Navbar bg="dark" variant="dark">
                <Container>
                    <Navbar.Brand href="#home">Face ID App - Computer Vision HSZG</Navbar.Brand>
                </Container>
            </Navbar>
            <Container className="flex-grow-1">
                <Row>
                    <Col>
                        <CameraComponent onCapture={handleValidation} />
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <MessageDisplay message={message} />
                    </Col>
                </Row>
            </Container>
            <div className="bg-dark text-white text-center py-3">
                © Mario Eduardo Diaz HSZG - 2023
            </div>
        </div>
    );
};

export default App;
