import React, { Component } from 'react';
import { Jumbotron, Button } from 'reactstrap';
import { Container, Row, Col } from 'reactstrap';

class ExpressionMatchView extends Component {
  render () {
    const imageURI = "http://143.215.48.102:5000/getmimic/" + this.props.imageID;

    return (
      <Container fluid={true}>
        <Row>
          <Jumbotron>
            <h1 className="display-3">wow this is trash</h1>
            <p className="lead">you have 5 seconds to match ur face to the image. points if its close go go go</p>    
            <hr className="my-2" />
            <img width={"100%"} src={imageURI}></img>
            <p className="lead">
            </p>
          </Jumbotron>
        </Row>
      </Container>

    );
  }
}

export default ExpressionMatchView;
