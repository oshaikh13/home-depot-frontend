import React, { Component } from 'react';
import Webcam from 'react-webcam';
import { Button } from 'reactstrap';
import { Container, Row, Col } from 'reactstrap';


class WebcamView extends Component {

  setRef = webcam => {
    this.webcam = webcam;
  };

  componentDidMount() {
    this.props.webcamLoaded(this.webcam);
  }

  render () {
    const videoConstraints = {
      width: 720,
      height: 720,
      facingMode: "user"
    };

    return (
      <Container fluid={true}>
        <Row>
          <Col style={{padding: 0}}>
            <Webcam 
              width="100%"
              height="100%"
              screenshotFormat="image/jpeg"
              videoConstraints={videoConstraints}
              screenshotQuality={1}
              ref={this.setRef}
            />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default WebcamView;