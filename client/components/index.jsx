import React from 'react'
import ReactDOM from 'react'


function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

const element = <Welcome name="world" />;
ReactDOM.render(
  element,
  document.getElementById('app')
);
