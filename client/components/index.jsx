import React from 'react';
import ReactDOM from 'react-dom';
import Signup from './authentication/Signup.jsx';


function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

const element = <Welcome name="world" />;
ReactDOM.render(
  <Signup />,
  document.getElementById('app')
);
