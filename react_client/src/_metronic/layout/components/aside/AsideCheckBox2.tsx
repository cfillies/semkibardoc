import { useState } from "react";

function AsideCheckBox2() {
  const [isCheckedOne, setIsCheckedOne] = useState(false);
  const [isCheckedTwo, setIsCheckedTwo] = useState(false);
  const [isCheckedThree, setIsCheckedThree] = useState(false);

  const handleOnChangeOne = () => {
    setIsCheckedOne(!isCheckedOne);
  };

  const handleOnChangeTwo = () => {
    setIsCheckedTwo(!isCheckedTwo);
  };

  const handleOnChangeThree = () => {
    setIsCheckedThree(!isCheckedThree);
  };

  return (
    <div className='menu-item'>
      <span className='menu-title fw-bolder' style={{ color: 'gray', margin: '20px' }}>Dokumenttyp:</span>
      <div 
        className='form-check form-check-solid'
        style={{margin: '20px'}}
      >
        <input
          className='form-check-input'  
          type="checkbox"
          id="topping2_1"
          name="topping2_1"
          value="Paneer2_1"
          checked={isCheckedOne}
          onChange={handleOnChangeOne}
        />
        <span className='menu-title' style={{ color: 'gray' }}>Objektschutz</span>
      </div>
      {/* <div className="result">
        Above checkbox is {isCheckedOne ? "checked" : "unchecked"}.
      </div> */}

      <div 
        className='form-check form-check-solid'
        style={{margin: '20px'}}
      >
        <input
          className='form-check-input'  
          type="checkbox"
          id="topping2"
          name="topping2_2"
          value="Paneer2_2"
          checked={isCheckedTwo}
          onChange={handleOnChangeTwo}
        />
        <span className='menu-title' style={{ color: 'gray' }}>Umgebungsschutz</span>
      </div>
      {/* <div className="result">
        Above checkbox is {isCheckedTwo ? "checked" : "unchecked"}.
      </div> */}

      <div 
        className='form-check form-check-solid'
        style={{margin: '20px'}}
      >
        <input
          className='form-check-input'  
          type="checkbox"
          id="topping2"
          name="topping2_3"
          value="Paneer2_3"
          checked={isCheckedThree}
          onChange={handleOnChangeThree}
        />
        <span className='menu-title' style={{ color: 'gray' }}>Andere</span>
      </div>
      {/* <div className="result">
        Above checkbox is {isCheckedTwo ? "checked" : "unchecked"}.
      </div> */}
    </div>
  );
}

export default AsideCheckBox2