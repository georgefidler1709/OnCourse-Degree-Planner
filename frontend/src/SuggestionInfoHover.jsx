// Modified from:
// https://gist.github.com/lou/571b7c0e7797860d6c555a9fdc0496f9

/*
* Usage:
* <SuggestionInfoHover
*    content={<div>Holy guacamole! I'm Sticky.</div>}
*    placement="top"
*    onMouseEnter={() => { }}
*    delay={200}
* >
*   <div>Show the sticky tooltip</div>
* </SuggestionInfoHover>
*/

import React, {Component} from 'react'
import { Overlay, Popover } from 'react-bootstrap'

class SuggestionInfoHover extends Component {
  constructor(props) {
    super(props)

    this.handleMouseEnter = this.handleMouseEnter.bind(this)
    this.handleMouseLeave = this.handleMouseLeave.bind(this)

    this.state = {
      showPopover: false,
    }
  }

  handleMouseEnter() {
    const {delay} = this.props

    this.setTimeoutConst = setTimeout(() => {
      this.setState({ showPopover: true }, () => {
      })
    }, delay);
  }

  handleMouseLeave() {
    clearTimeout(this.setTimeoutConst)
    this.setState({ showPopover: false })
  }

  componentWillUnmount() {
    if (this.setTimeoutConst) {
      clearTimeout(this.setTimeoutConst)
    }
  }

  render() {
    let { content, children, placement } = this.props

    const child = React.Children.map(children, (child) => (
      React.cloneElement(child, {
        onMouseEnter: this.handleMouseEnter,
        onMouseLeave: this.handleMouseLeave,
        ref: (node) => {
          this._child = node
          const { ref } = child
          if (typeof ref === 'function') {
            ref(node);
          }
        }
      })
    ))[0]

    return(
      <React.Fragment>
        {child}
        <Overlay
          show={this.state.showPopover}
          placement={placement}
          target={this._child}
          shouldUpdatePosition={true}
        >
          <Popover
            onMouseEnter={() => {
              this.setState({ showPopover: true })
            }}
            onMouseLeave={this.handleMouseLeave}
            id='popover'
          >
            <Popover.Content>{content}</Popover.Content>
          </Popover>
        </Overlay>
      </React.Fragment>
    )
  }
}

export default SuggestionInfoHover