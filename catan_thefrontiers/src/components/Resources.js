import React from 'react'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import 'bootstrap/dist/css/bootstrap.min.css'
import Card from 'react-bootstrap/Card'
import CardDeck from 'react-bootstrap/CardDeck'
import Navbar from 'react-bootstrap/Navbar'

export default class Resources extends React.Component {
    render() {
        return (
            <div>
                <Navbar bg="dark" variant="dark">
                    <Navbar.Brand>
                        <img
                            alt=""
                            src="/img/icon.png"
                            width="30"
                            height="30"
                            className="d-inline-block align-top"
                        />
                        {' Recursos'}
                    </Navbar.Brand>
                </Navbar>
                <Container fluid="true" style={{marginTop:'10px'}}>
                    <Row>
                        <CardDeck>
                            <Card bg="dark" text="light"
                                border="info" style={{ borderRadius: 30 }}>
                                <Card.Img style={{
                                    minHeight: '13rem', borderRadius:30
                                }} variant="top" src="/img/wood.jpeg" />
                                <Card.Header as="h5">Madera</Card.Header>
                                <Card.Body>
                                    <Card.Text>
                                        Cantidad: {this.props.res.lumber}
                                    </Card.Text>
                                </Card.Body>
                            </Card>

                            <Card bg="dark" text="light"
                                border="info" style={{ borderRadius: 30 }}>
                                <Card.Img style={{
                                    minHeight: '13rem',  borderRadius:30
                                }} variant="top" src="/img/wool.jpeg" />
                                <Card.Header as="h5">Lana</Card.Header>
                                <Card.Body>
                                    <Card.Text>
                                        Cantidad: {this.props.res.wool}
                                    </Card.Text>
                                </Card.Body>
                            </Card>

                            <Card bg="dark" text="light"
                                border="info" style={{ borderRadius: 30 }}>
                                <Card.Img style={{
                                    minHeight: '13rem',  borderRadius:30
                                }} variant="top" src="/img/minerals.jpg" />
                                <Card.Header as="h5">Minerales</Card.Header>
                                <Card.Body>
                                    <Card.Text>
                                        Cantidad: {this.props.res.ore}
                                    </Card.Text>
                                </Card.Body>
                            </Card>

                            <Card bg="dark" text="light"
                                border="info" style={{ borderRadius: 30 }}>
                                <Card.Img style={{
                                    minHeight: '13rem',  borderRadius:30
                                }} variant="top" src="/img/cereals.jpg" />
                                <Card.Header as="h5">Cereales</Card.Header>
                                <Card.Body>
                                    <Card.Text>
                                        Cantidad: {this.props.res.grain}
                                    </Card.Text>
                                </Card.Body>
                            </Card>

                            <Card bg="dark" text="light"
                                border="info" style={{ borderRadius: 30 }}>
                                <Card.Img style={{
                                    minHeight: '13rem',  borderRadius:30
                                }} variant="top" src="/img/clay.jpg" />
                                <Card.Header as="h5">Arcilla</Card.Header>
                                <Card.Body>
                                    <Card.Text>
                                        Cantidad: {this.props.res.brick}
                                    </Card.Text>
                                </Card.Body>
                            </Card>
                        </CardDeck>
                    </Row>
                </Container>
            </div>)
    }
}
