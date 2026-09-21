export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate, proxy-revalidate");
  res.setHeader("Pragma", "no-cache");
  res.setHeader("Expires", "0");

  if (req.method === "OPTIONS") {
    res.status(200).end();
    return;
  }

  const EDGE_CONFIG_ID = "ecfg_tswb1xrqrug1hh8ha4kvxsvcv81q";
  const READ_TOKEN = "7efde2d8-d8ab-4a19-8b2f-0d8e1de105e3";
  const WRITE_TOKEN = process.env.VERCEL_API_TOKEN;

  if (req.method === "GET") {
    try {
      const response = await fetch(`https://edge-config.vercel.com/${EDGE_CONFIG_ID}/item/projects`, {
        headers: { Authorization: `Bearer ${READ_TOKEN}` },
        cache: "no-store"
      });
      if (!response.ok) {
        return res.status(200).json({ success: false, data: null });
      }
      const data = await response.json();
      return res.status(200).json({ success: true, data: data });
    } catch (e) {
      return res.status(500).json({ success: false, error: e.message });
    }
  }

  if (req.method === "POST") {
    try {
      let projectsData = req.body;
      if (typeof projectsData === "string") {
        projectsData = JSON.parse(projectsData);
      }
      if (projectsData && projectsData.projects) {
        projectsData = projectsData.projects;
      }

      if (!Array.isArray(projectsData)) {
        return res.status(400).json({ success: false, error: "Data harus berupa array proyek" });
      }

      const patchRes = await fetch(`https://api.vercel.com/v1/edge-config/${EDGE_CONFIG_ID}/items`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${WRITE_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          items: [
            {
              operation: "upsert",
              key: "projects",
              value: projectsData
            }
          ]
        })
      });

      if (!patchRes.ok) {
        const errText = await patchRes.text();
        return res.status(patchRes.status).json({ success: false, error: errText });
      }

      return res.status(200).json({ success: true, count: projectsData.length });
    } catch (e) {
      return res.status(500).json({ success: false, error: e.message });
    }
  }

  res.status(405).json({ error: "Method not allowed" });
}
