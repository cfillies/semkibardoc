import { useState } from "react";

function AsideCheckBox() {
  const [isCheckedOne, setIsCheckedOne] = useState(false);
  const [isCheckedTwo, setIsCheckedTwo] = useState(false);

  const handleOnChangeOne = () => {
    setIsCheckedOne(!isCheckedOne);
  };

  const handleOnChangeTwo = () => {
    setIsCheckedTwo(!isCheckedTwo);
  };

  return (
    <div className='menu-item'>
      <span className='menu-title fw-bolder' style={{ color: 'gray', margin: '20px' }}>Filter nach:</span>
      <div 
        className='form-check form-check-solid'
        style={{margin: '20px'}}
      >
        <input
          className='form-check-input'  
          type="checkbox"
          id="topping1"
          name="topping1"
          value="Paneer1"
          checked={isCheckedOne}
          onChange={handleOnChangeOne}
        />
        <span className='menu-title' style={{ color: 'gray' }}>Vorgangsdokumente</span>
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
          name="topping2"
          value="Paneer2"
          checked={isCheckedTwo}
          onChange={handleOnChangeTwo}
        />
        <span className='menu-title' style={{ color: 'gray' }}>Nicht Vorgang relevante Dokumente</span>
      </div>
      {/* <div className="result">
        Above checkbox is {isCheckedTwo ? "checked" : "unchecked"}.
      </div> */}
    </div>
  );
}

export default AsideCheckBox