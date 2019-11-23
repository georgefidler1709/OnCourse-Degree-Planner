/**
 * COMP4290 Group Project
 * Team: On Course
 * Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910), 
 * George Fidler (z5160384), Kevin Ni (z5025098)
 *
 * SuggestionInfoHover.tsx
 * Implements a suggestion when you hover over a search result that takes you to
 * a link with more information.
 *
 * Modified from: https://gist.github.com/lou/571b7c0e7797860d6c555a9fdc0496f9
 */

import React, {Component, RefObject} from 'react'
import { Overlay, Popover } from 'react-bootstrap'
import { Position } from '../../Types'
import CSS from 'csstype'

interface SuggestionInfoHoverProps { 
  content: JSX.Element
  placement?: Position
  delay: number
  children: JSX.Element
  key: string
  infoSize: CSS.Properties 
}

/**
 * Implements a pop-up with URL to more information when you hover over a search result.
 */
class SuggestionInfoHover extends Component<SuggestionInfoHoverProps, {showPopover: boolean}> {
  private setTimeoutConst?: ReturnType<typeof setTimeout>
  private targetRef: RefObject<Component>

  /**
   * Initialises state, binds functions, creates a reference.
   */
  constructor(props: SuggestionInfoHoverProps) {
    super(props)

    this.handleMouseEnter = this.handleMouseEnter.bind(this)
    this.handleMouseLeave = this.handleMouseLeave.bind(this)
    this.targetRef = React.createRef()

    this.state = {
      showPopover: false,
    }
  }

  /**
   * Reaction to mouse entering the hover area.
   */
  handleMouseEnter() {
    const {delay} = this.props

    this.setTimeoutConst = setTimeout(() => {
      this.setState({ showPopover: true }, () => {
      })
    }, delay);
  }

  /**
   * Reaction to mouse leaving the hover area.
   */
  handleMouseLeave() {
    if(this.setTimeoutConst) {
      clearTimeout(this.setTimeoutConst)
    }
    this.setState({ showPopover: false })
  }

  /**
   * Making sure hover suggestion times out.
   */
  componentWillUnmount() {
    if (this.setTimeoutConst) {
      clearTimeout(this.setTimeoutConst)
    }
  }

  /**
   * HTML look of the hover
   */
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
            <Popover.Content style={this.props.infoSize}>{content}</Popover.Content>
          </Popover>
        </Overlay>
      </React.Fragment>
    )
  }
}

export default SuggestionInfoHover
