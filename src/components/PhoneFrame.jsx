export default function PhoneFrame({ children }) {
  return (
    <div className="phone-stage">
      <div className="phone-frame">
        <div className="phone-notch" />
        {children}
      </div>
    </div>
  )
}
