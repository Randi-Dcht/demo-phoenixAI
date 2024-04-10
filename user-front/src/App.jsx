import axios from 'axios'
import { useForm } from 'react-hook-form'
import './App.css'
import {useState} from "react";

function App() {
       const { register, handleSubmit } = useForm();
       const [result, setResult] = useState([]);
       const [url, setUrl] = useState('http://localhost:5050');

    const onSubmit = async (data) => {
        const formData = new FormData();
        formData.append('file', data.file[0]);

        try {
            const response = await axios.post(url + '/predict/image', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Accept': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
            });
            response.data.forEach((prediction) => {
                setResult(prediction.result);
                console.log(prediction.result)
            });
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    return (
        <>
            <input type="text" defaultValue={url} onChange={(e) => setUrl(e.target.value)}/>
            <form className="is-centered is-center" onSubmit={handleSubmit(onSubmit)}>
                <input type="file" {...register('file')} accept="image/jpeg" required/>
                <button className="button is-primary mt-3" type="submit">test</button>
            </form>
            <div>
                <h4>Result</h4>
                <div>
                    {result.map((item, index) => (
                        <div key={index}>
                            <p>{item}</p>
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
}

export default App
