using UnityEngine;
using System.IO;
public class FileManager : MonoBehaviour
{
    //Metodo para guardar los datos
    public void GuardarData()
    {
        string ruta = Application.persistentDataPath + "/playerData.json";
        
        PlayerData data = new PlayerData(gameManager.instance.getMonedasUsables(),
            gameManager.instance.tiempoGuardar,
            gameManager.instance.canDash,
            gameManager.instance.dobleSaltos);
    
        string jsonDatos = JsonUtility.ToJson(data,true);

        File.WriteAllText(ruta,jsonDatos);
        Debug.Log("Se guardo la data");
    }

    //Metodo para cargar los datos
    public void CargarData()
    {
        string ruta = Application.persistentDataPath + "/playerData.json";

        if (File.Exists(ruta))
        {
            string jsonDatos = File.ReadAllText(ruta);

            PlayerData data = JsonUtility.FromJson<PlayerData>(jsonDatos);

            gameManager.instance.tiempoGuardar = data.puntajeAlto;
            gameManager.instance.monedasUsables = data.monedasUsables;
            gameManager.instance.canDash = data.canDash;
            gameManager.instance.dobleSaltos = data.doblesSaltos;
            //Esto lo imprimo en consola para mostrar la ruta para eliminar el archivo de guardado
            Debug.Log("Ruta de persistentDataPath: " + Application.persistentDataPath);

        }
        else {

            Debug.Log("No se encontro el archivo");
        }
    }
}
