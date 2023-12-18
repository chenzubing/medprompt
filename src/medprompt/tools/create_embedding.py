"""
 Copyright 2023 Bell Eapen

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import os
import logging
from kink import di
from typing import Any, Optional, Type
from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun,
                                         CallbackManagerForToolRun)
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.tools import BaseTool
from langchain.vectorstores import Redis, Chroma, FAISS
from langchain.pydantic_v1 import BaseModel, Field
from .. import MedPrompter, get_time_diff_from_today

class SearchInput(BaseModel):
    patient_id: str = Field()

class CreateEmbeddingFromFhirBundle(BaseTool):
    """
    Creates an embedding for a patient with id.
    """
    name = "create index for medical record"
    description = """
    Creates a medical record index for a patient with patient_id.
    """
    args_schema: Type[BaseModel] = SearchInput

    # Embedding model
    EMBED_MODEL = di["embedding_model"]

    # Create vectorstore
    embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # Index schema
    INDEX_SCHEMA = di["index_schema"]
    VECTORSTORE_NAME = di["vectorstore_name"]
    REDIS_URL = di["redis_url"]

    def _run(
            self,
            patient_id: str = None,
            run_manager: Optional[CallbackManagerForToolRun] = None
            ) -> str:
        prompt = MedPrompter()
        chunks = []
        try:
            get_medical_record_tool = di["get_medical_record_tool"]
            bundle_input = get_medical_record_tool._run(patient_id=patient_id)
        except:
            return "Sorry, Create Embedding needs an implementation of Get Medical Record Tool."
        try:
            for entry in bundle_input["entry"]:
                resource = entry["resource"]

                if resource["resourceType"] == "Patient" or resource["resourceType"] == "Observation" \
                    or resource["resourceType"] == "DocumentReference":
                    resource["time_diff"] = get_time_diff_from_today
                    template_name = resource['resourceType'].lower() + "_v1.jinja"
                    prompt.set_template(template_name=template_name)
                    chunk = {
                        "page_content": prompt.generate_prompt(resource).replace("\n", " "),
                        "metadata": {
                            "resourceType": resource["resourceType"],
                            "resourceID": str(resource["id"]),
                            "patientID": str(patient_id)
                        }
                    }
                    chunks.append(chunk)
        except:
            logging.info("No Data found for patient with id: " + patient_id)
            return chunks
        logging.info("No of resources found for patient: " + str(len(chunks)))
        try:
            # Store in Redis
            if self.VECTORSTORE_NAME == "redis":
                db = Redis.from_texts(
                    # appending this little bit can sometimes help with semantic retrieval
                    # especially with multiple companies
                    # texts=[f"Company: {company_name}. " + chunk["page_content"] for chunk in chunks],
                    texts=[chunk["page_content"] for chunk in chunks],
                    metadatas=[chunk["metadata"] for chunk in chunks],
                    embedding=self.embedder,
                    index_name=patient_id,
                    # index_schema=self.INDEX_SCHEMA,
                    redis_url=self.REDIS_URL
                )
                db.write_schema(self.INDEX_SCHEMA)

            # Store in Chroma
            elif self.VECTORSTORE_NAME == "chroma":
                db = Chroma.from_texts(
                    persist_directory=di["vectorstore_path"],
                    texts=[chunk["page_content"] for chunk in chunks],
                    metadatas=[chunk["metadata"] for chunk in chunks],
                    embedding=self.embedder,
                    ids=[chunk["metadata"]["resourceID"] for chunk in chunks],
                    collection_name=patient_id
                )

            # Store in FAISS
            elif self.VECTORSTORE_NAME == "faiss":
                fname = di["vectorstore_path"] + "/" + patient_id + ".index"
                if not os.path.exists(fname):
                    db = FAISS.from_texts(
                        texts=[chunk["page_content"] for chunk in chunks],
                        metadatas=[chunk["metadata"] for chunk in chunks],
                        embedding=self.embedder,
                    )
                    db.save_local(fname)
            else:
                logging.info("No vector store found for patient with id: " + patient_id)
                # return "No vector store found for patient with id: {}".format(patient_id)
                raise Exception("No vector store found for patient with id: {}".format(patient_id))
        except Exception as e:
            logging.info("Unable to create embedding for patient with id: " + patient_id)
            # return "Unable to create embedding for patient with id: {}".format(patient_id)
            raise Exception("Unable to create embedding for patient with id: {}".format(patient_id))
        logging.info("Embeddings created for patient with id: " + patient_id)
        return "Embeddings created for patient with id: {}".format(patient_id)
    async def _arun(
            self,
            patient_id: str = None,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None
            ) -> Any:
        raise NotImplementedError("Async not implemented yet")
        # return self._run(patient_id, run_manager)