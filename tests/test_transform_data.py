import unittest
from transformation.transform_data import transform_data

class TestTransformData(unittest.TestCase):

    def test_transform_data_valid(self):
        """Test transformation with a valid CVE dataset"""
        input_data = {
            "vulnerabilities": [
                {
                    "cve": {
                        "id": "CVE-2024-0001",
                        "sourceIdentifier": "nvd@nist.gov",
                        "published": "2024-02-15T10:00:00.000Z",
                        "lastModified": "2024-02-16T10:00:00.000Z",
                        "vulnStatus": "Analyzed",
                        "descriptions": [{"lang": "en", "value": "Example vulnerability"}],
                        "metrics": {
                            "cvssMetricV31": [
                                {
                                    "cvssData": {
                                        "version": "3.1",
                                        "vectorString": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                                        "attackVector": "NETWORK",
                                        "attackComplexity": "LOW",
                                        "privilegesRequired": "NONE",
                                        "userInteraction": "NONE",
                                        "scope": "UNCHANGED",
                                        "confidentialityImpact": "HIGH",
                                        "integrityImpact": "HIGH",
                                        "availabilityImpact": "HIGH",
                                        "baseScore": 9.8,
                                        "baseSeverity": "CRITICAL"
                                    },
                                    "exploitabilityScore": 3.9,
                                    "impactScore": 5.9
                                }
                            ]
                        },
                        "weaknesses": [{"source": "NVD", "description": [{"value": "CWE-79"}]}],
                        "configurations": [
                            {
                                "operator": "OR",
                                "negate": False,
                                "nodes": [
                                    {
                                        "cpeMatch": [
                                            {
                                                "criteria": "cpe:2.3:o:vendor:product:1.0",
                                                "vulnerable": True
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "references": [{"url": "http://example.com", "source": "NVD", "tags": ["Patch"]}]
                    }
                }
            ]
        }

        result = transform_data(input_data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["cve_id"], "CVE-2024-0001")
        self.assertEqual(result[0]["source_identifier"], "nvd@nist.gov")
        self.assertEqual(result[0]["published"], "2024-02-15T10:00:00.000Z")
        self.assertEqual(result[0]["metrics"][0]["base_score"], 9.8)
        self.assertEqual(result[0]["weaknesses"][0]["description"], "CWE-79")
        self.assertEqual(result[0]["configurations"][0]["criteria"], "cpe:2.3:o:vendor:product:1.0")
        self.assertEqual(result[0]["references"][0]["url"], "http://example.com")

    def test_transform_data_empty(self):
        """Test transformation with empty input"""
        input_data = {}
        result = transform_data(input_data)
        self.assertEqual(result, [])

    def test_transform_data_missing_fields(self):
        """Test transformation with missing fields"""
        input_data = {
            "vulnerabilities": [
                {
                    "cve": {
                        "id": "CVE-2024-0002",
                        "metrics": {},
                        "configurations": []
                    }
                }
            ]
        }
        
        result = transform_data(input_data)

        self.assertEqual(result[0]["cve_id"], "CVE-2024-0002")
        self.assertEqual(result[0]["descriptions"], [])
        self.assertEqual(result[0]["metrics"], [])
        self.assertEqual(result[0]["weaknesses"], [])
        self.assertEqual(result[0]["configurations"], [])

if __name__ == "__main__":
    unittest.main()
