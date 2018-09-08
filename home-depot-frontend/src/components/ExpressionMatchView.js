import React, { Component } from 'react';
import { Jumbotron, Button } from 'reactstrap';
import { Container, Row, Col } from 'reactstrap';

class ExpressionMatchView extends Component {
  render () {
    const imageURI = "http://143.215.48.102:5000/getmimic/" + this.props.imageID;

    return (
          <Jumbotron>
            <h1 className="display-3">MemeMatch {this.props.imageID}/{this.props.totalImages}</h1>  
            <hr className="my-2" />
            <img width={"100%"} src={imageURI}></img>
            <p className="lead">
            </p>
          </Jumbotron>
    );
  }
}

export default ExpressionMatchView;
