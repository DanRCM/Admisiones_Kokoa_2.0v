using UnityEngine;



public class autodestruccion : MonoBehaviour
{

    // El nombre de este script es muy descriptivo, lo uso  en algunas animaciones. si es una transicion hago que se mantenga a pesar de pasar de escena.
    public float time = 1.2f;
    public bool transicion;
    void Start()
    {
        if (transicion)
        {
            DontDestroyOnLoad(gameObject);
        }
        Invoke("autodestruyete",time);
    }

    private void autodestruyete() 
    { 
        Destroy(gameObject);
    }
   
}
