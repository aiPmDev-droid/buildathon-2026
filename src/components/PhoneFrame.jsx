import BottomTabBar from "./BottomTabBar"

export default function PhoneFrame({ active, onChange, showTabBar = true, children }) {
  return (
    <div className="phone-stage">
      <div className="phone-frame">
        <div className="phone-orbs" aria-hidden="true">
          <span className="phone-orb phone-orb-blue-1" />
          <span className="phone-orb phone-orb-gold-1" />
          <span className="phone-orb phone-orb-blue-2" />
          <span className="phone-orb phone-orb-gold-2" />
        </div>
        <div className="phone-notch" />
        <div className="phone-content">{children}</div>
        {showTabBar && <BottomTabBar active={active} onChange={onChange} />}
      </div>
    </div>
  )
}
