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
                <h2> Signup page for collabpro </h2>
                <form>
                    <input name="firstname" placeholder="firstname" type="text" />
                    </form>
            </div>
        )
       
    }
}
