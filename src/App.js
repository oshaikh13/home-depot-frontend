import React, { Component } from 'react';
import './App.css';
import { Container, Row, Col } from 'reactstrap';
import WebcamView from './components/WebcamView'
import ExpressionMatchView from './components/ExpressionMatchView'
import request from 'request';


class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      timeLeft: 10,
      defaultCountdown: 10,
      totalImages: 4,
      mimic: null,
      usermimic: null,
      r: 0,
      imageID: 1,
      points: 0
    };
  }

  loadNextImage = () => {
    if (this.state.timeLeft > 0) {
      this.setState({ timeLeft: this.state.timeLeft - 1 });
      return;
    } 

    const imageSrc = this.webcam.getScreenshot();
    request.post('http://143.215.48.102:5000/compare', {
      body: {
        img: imageSrc,
        id: this.state.imageID
      },
      json: true   
    }, (err, res, body) => {
      const nextID = this.state.imageID + 1;
      let newState = {
        imageID: nextID,
        mimic: body.mimic, 
        usermimic: body.user_mimic, 
        timeLeft: this.state.defaultCountdown,
        points: this.state.points,
        r: body.r[0]
      }

      
      if (this.state.r > .6) {
        newState.points = this.state.points + 1;
      }

      if (nextID > this.state.totalImages) {
        alert("game's over bois. you got " + newState.points + " points. hit okay to give it another go.")
        newState = {
          imageID: 1,
          timeLeft: 5,
          r: 0,
          points: 0
        }
      }

      this.setState(newState);

    });


  }

  componentDidMount () {
    this.interval = setInterval(this.loadNextImage, 1000);
  }

  webcamLoaded  = (webcam) => {
    this.webcam = webcam;
  }

  componentWillUnmount () {
    clearInterval(this.interval);
  }

  render () {
    return (
      <Container fluid={true}>
        <Row>
          <Col style={{padding: 0}}>
            <ExpressionMatchView imageID={this.state.imageID} r={this.state.r} totalImages={this.state.totalImages} 
              points={this.state.points} />
          </Col>
          <Col style={{padding: 0}}>
            <WebcamView webcamLoaded={this.webcamLoaded} imageID={this.state.imageID} />
            <h3>seconds left: {this.state.timeLeft}</h3>
            <p>lets goooo numero {this.state.imageID}/{this.state.totalImages}</p>
            <p>points: {this.state.points}</p>
            <p>R correlation (aim for > .6) {this.state.r}</p>     
          </Col>
        </Row>
      </Container>
    );
  }
}

export default App;
