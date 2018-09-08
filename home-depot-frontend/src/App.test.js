import React from 'react';
import ReactDOM from 'react-dom';
import ExpressionMatchView from './components/ExpressionMatchView';

it('renders without crashing -- expressionmatchview', () => {
  const div = document.createElement('div');
  ReactDOM.render(<ExpressionMatchView />, div);
  ReactDOM.unmountComponentAtNode(div);
});
