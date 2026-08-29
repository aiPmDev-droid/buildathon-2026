import BottomTabBar from "./BottomTabBar"

export default function PhoneFrame({ active, onChange, showTabBar = true, children }) {
  return (
    <div className="phone-stage">
      <div className="phone-frame">
        <div className="phone-notch" />
        <div className="phone-content">{children}</div>
        {showTabBar && <BottomTabBar active={active} onChange={onChange} />}
      </div>
    </div>
  )
}
