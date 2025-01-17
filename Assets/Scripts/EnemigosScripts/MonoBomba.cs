using System.Collections;
using UnityEngine;

public class MonoBomba : MonoBehaviour
{
    public GameObject bombaPrefab;
    public Transform spawn;
    public bool puedeLanzar;
    void Start()
    {
        puedeLanzar = true;
    }

    // Update is called once per frame
    void Update()
    {
        if (puedeLanzar)
        {
            StartCoroutine(bombas());
        }    
    }

    IEnumerator bombas()
    {
        puedeLanzar=false;
        Instantiate(bombaPrefab, spawn.position, spawn.rotation);
        yield return new WaitForSeconds(3f);
        puedeLanzar = true ;
    }
}
