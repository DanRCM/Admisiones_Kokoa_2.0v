using System.IO;
using UnityEngine;
using UnityEngine.UI;

public class MenuInicial : MonoBehaviour
{

    public Slider musicSlider, sfxSlider;
    public float valueSfx, valueVolumen;
    public GameObject cargar;
    private void Start()
    {
        cargarSonidoPref();
        
        cargar.SetActive(true);
        Invoke("cargador", 1f);
    }
    
    public void cargador()
    {
        cargar.SetActive(false);
    }   
    
    public void volumenMusica()
    {
        if (musicSlider != null)
        {
            valueVolumen = Mathf.Log10(musicSlider.value * 9 + 1);
            AudioManager.instance.musicVolumen(valueVolumen);
            guardarSonidoPref();
        }

    }
    public void volumenfx()
    {
        if (sfxSlider != null)
        {
            valueSfx = Mathf.Log10(sfxSlider.value * 9 + 1);
            AudioManager.instance.sfxSound(valueSfx);
            guardarSonidoPref();
        }

    }
    public void iniciar()
    {
        AudioManager.instance.PlaySfx("boton");
        gameManager.instance.cargarEscena();
    }
    public void sonidoBoton()
    {
        AudioManager.instance.PlaySfx("boton");
    }

   
    public void Salir()
    {
        //Se guarda los datos del usuario
        AudioManager.instance.PlaySfx("boton");
        gameManager.instance.fileManager.GuardarData();
        Application.Quit();
        //Debug.log es para mostrar por consola que si se activo esta funcion
        Debug.Log("Esta saliendo");


    }


   
    //Funcion para cargar la preferencia del sonido que tenga la persona
    public void cargarSonidoPref()
    {
        string ruta = Application.persistentDataPath + "/sonido.json";

        if (File.Exists(ruta))
        {
            string jsonDatos = File.ReadAllText(ruta);
            if (musicSlider != null && sfxSlider != null)
            {
                SonidoPref sonidopref = JsonUtility.FromJson<SonidoPref>(jsonDatos);
                musicSlider.value = sonidopref.musicVolumen;
                sfxSlider.value = sonidopref.sfxVolume;
                valueSfx = sonidopref.sfxVolume;
                valueVolumen = sonidopref.musicVolumen;

            }


            volumenfx();
            volumenMusica();

            //Esto lo imprimo en consola para mostrar la ruta para eliminar el archivo de guardado
            Debug.Log("Ruta de persistentDataPath: " + Application.persistentDataPath);

        }
        else
        {

            Debug.Log("No se encontro el archivo");
        }
    }

    //Esto guarda el sonido
    public void guardarSonidoPref()
    {
        string ruta = Application.persistentDataPath + "/sonido.json";
        SonidoPref sonidopref = new SonidoPref(valueSfx,valueVolumen);
        string jsonDatos = JsonUtility.ToJson(sonidopref, true);
        File.WriteAllText(ruta, jsonDatos);
        Debug.Log("Se guardo las preferencias");
    }
}
