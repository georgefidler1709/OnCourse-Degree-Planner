// Modified from:
// https://gist.github.com/lou/571b7c0e7797860d6c555a9fdc0496f9

/*
* Usage:
* <SuggestionInfoHover
*    content={<div>Holy guacamole! I'm Sticky.</div>}
*    placement="top"
*    delay={200}
* >
*   <div>Show the sticky tooltip</div>
* </SuggestionInfoHover>
*/

import React, {Component, RefObject} from 'react'
import { Overlay, Popover } from 'react-bootstrap'
import { Position } from '../../Types'


interface SuggestionInfoHoverProps { 
  content: JSX.Element
  placement?: Position
  delay: number
  children: JSX.Element
  key: string
}

class SuggestionInfoHover extends Component<SuggestionInfoHoverProps, {showPopover: boolean}> {
  private setTimeoutConst?: ReturnType<typeof setTimeout>
  private targetRef: RefObject<Component>

  constructor(props: SuggestionInfoHoverProps) {
    super(props)

    this.handleMouseEnter = this.handleMouseEnter.bind(this)
    this.handleMouseLeave = this.handleMouseLeave.bind(this)
    this.targetRef = React.createRef()

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
    if(this.setTimeoutConst) {
      clearTimeout(this.setTimeoutConst)
    }
    this.setState({ showPopover: false })
  }

  componentWillUnmount() {
    if (this.setTimeoutConst) {
      clearTimeout(this.setTimeoutConst)
    }
  }

  render() {
    let { content, children, placement } = this.props

    return(
      <React.Fragment>
        {React.cloneElement(children, {
          onMouseEnter: this.handleMouseEnter,
          onMouseLeave: this.handleMouseLeave,
          ref: this.targetRef
        })}
        <Overlay
          show={this.state.showPopover}
          placement={placement}
          target={this.targetRef.current!}
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
