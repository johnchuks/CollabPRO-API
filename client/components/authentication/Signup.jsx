import React, { Component } from 'react'


export default class Signup extends Component {
    constructor(props) {
        super(props);
        this.state = {
            firstName: '',
            lastName: '',
            userName: '',
            email: '',
            password: ''
        }
    }

    render() {
        return(
            <div>
            <h2> Welcome to React!!!!!!</h2>
            </div>
        )
       
    }
}
