import {useState} from 'react'
import './Izvjesce_app.css'


function Izvjesce_app() {

    function handleVodovod(){

    }
    function handleZgrada(){

    }

  return (
    <div className="App">

        <div className="Pictures">
            <img className="pic1" src="/pictures/izvjesce_vodovod.png"/>
            <img className="pic2" src="/pictures/izvjesce_zgrada.png"/>
        </div>

        <div>
            <div className="btn1">
                <button className= "btn btn-primary" onClick={handleVodovod}> Generiraj izvještaj za vodovod </button>
            </div>
            <div className="btn2">
                <button className= "btn btn-primary1" onClick={handleZgrada}> Generiraj izvještaj za zgradu </button>
            </div>
        </div>
        <div className="Generated">


        </div>

    </div>
  )
}

export default Izvjesce_app

