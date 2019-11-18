import React from 'react'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import 'bootstrap/dist/css/bootstrap.min.css'
import Card from 'react-bootstrap/Card'
import CardDeck from 'react-bootstrap/CardDeck'
import Navbar from 'react-bootstrap/Navbar'

export default class Cards extends React.Component {
    render() {
        return (
            <div>
                <Navbar bg="dark" variant="dark">
                    <Navbar.Brand>
                        <img
                            alt=""
                            src="/img/card.png"
                            width="30"
                            height="30"
                            className="d-inline-block align-top"
                            style={{ marginRight: 10 }}
                        />
                        Cartas
                    </Navbar.Brand>
                </Navbar>
                <Container fluid="true" style={{ marginTop: '10px' }}>
                    <Row>
                        <CardDeck>
                            <Card bg="dark" text="light"
                                border="info" style={{ borderRadius: 30 }}>
                                <Card.Img style={{
                                    minHeight: '13rem', borderRadius: 30
                                }} variant="top" src={"/img/road_building.jpg"} />
                                <Card.Body>
                                    <Card.Text>
                                        Cantidad: {this.props.cards.road_building}
                                    </Card.Text>
                                </Card.Body>
                            </Card>
                            <Card bg="dark" text="light"
                                border="info" style={{ borderRadius: 30 }}>
                                <Card.Img style={{
                                    minHeight: '13rem', borderRadius: 30
                                }} variant="top" src={"/img/year_of_plenty.jpg"} />
                                <Card.Body>
                                    <Card.Text>
                                        Cantidad: {this.props.cards.year_of_plenty}
                                    </Card.Text>
                                </Card.Body>
                            </Card>
                            <Card bg="dark" text="light"
                                border="info" style={{ borderRadius: 30 }}>
                                <Card.Img style={{
                                    minHeight: '13rem', borderRadius: 30
                                }} variant="top" src={"/img/monopoly.jpg"} />
                                <Card.Body>
                                    <Card.Text>
                                        Cantidad: {this.props.cards.monopoly}
                                    </Card.Text>
                                </Card.Body>
                            </Card>
                            <Card bg="dark" text="light"
                                border="info" style={{ borderRadius: 30 }}>
                                <Card.Img style={{
                                    minHeight: '13rem', borderRadius: 30
                                }} variant="top" src={"/img/victory_point.jpg"} />
                                <Card.Body>
                                    <Card.Text>
                                        Cantidad: {this.props.cards.victory_point}
                                    </Card.Text>
                                </Card.Body>
                            </Card>
                            <Card bg="dark" text="light"
                                border="info" style={{ borderRadius: 30 }}>
                                <Card.Img style={{
                                    minHeight: '13rem', borderRadius: 30
                                }} variant="top" src={"/img/knight.jpg"} />
                                <Card.Body>
                                    <Card.Text>
                                        Cantidad: {this.props.cards.knight}
                                    </Card.Text>
                                </Card.Body>
                            </Card>
                        </CardDeck>
                    </Row>
                </Container>
            </div>)
    }
}
