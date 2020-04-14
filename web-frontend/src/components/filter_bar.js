import React from "react"
import moment from "moment"


const DATE_FIELD_FORMAT = "YYYY-MM-DD"


export default ({ totalCount, filteredCount, loading, minFromDate, fromDate, toDate, setFromDate, setToDate, setLoading }) => {

  const todayString = moment().format(DATE_FIELD_FORMAT)
  const minFromDateString = moment(minFromDate).format(DATE_FIELD_FORMAT)
  const fromDateString = moment(fromDate).format(DATE_FIELD_FORMAT)
  const toDateString = moment(toDate).format(DATE_FIELD_FORMAT)

  return (
    <nav className="level">
      <div className="level-left">
        <p className="title is-4 has-text-white">
          {filteredCount} Pest Sightings ({totalCount} Total)
        </p>
      </div>
      <div className="level-right">
        <div className="level-item">
          <div className="field has-addons">
            <p className="control">
              <button className="button is-static">From</button>
            </p>
            <p className="control">
              <input className="input" type="date" min={minFromDateString} value={fromDateString}
                onChange={(e) => {
                  setFromDate(moment(e.target.value))
                  setLoading(true)
                }} />
            </p>
          </div>
        </div>
        <div className="level-item">
          <div className="field has-addons">
            <p className="control">
              <button className="button is-static">To</button>
            </p>
            <p className="control">
              <input className="input" type="date" min={fromDateString} max={todayString} value={toDateString}
                onChange={(e) => {
                  setToDate(moment(e.target.value))
                  setLoading(true)
                }} />
            </p>
          </div>
        </div>
        <div className="level-item">
          <button className={`button ` + (loading ? `is-loading` : ``)} onClick={() => setLoading(true)}>
            Refresh
          </button>
        </div>
      </div>
    </nav>
  )
}