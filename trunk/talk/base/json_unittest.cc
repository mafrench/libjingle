/*
 * libjingle
 * Copyright 2009, Google Inc.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *  1. Redistributions of source code must retain the above copyright notice,
 *     this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright notice,
 *     this list of conditions and the following disclaimer in the documentation
 *     and/or other materials provided with the distribution.
 *  3. The name of the author may not be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
 * EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
 * ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include <vector>
#include "talk/base/gunit.h"
#include "talk/base/json.h"

static Json::Value in_s("foo");
static Json::Value in_sn("99");
static Json::Value in_si("-99");
static Json::Value in_sb("true");
static Json::Value in_sd("1.2");
static Json::Value in_n(12);
static Json::Value in_i(-12);
static Json::Value in_u(34U);
static Json::Value in_b(true);
static Json::Value in_d(1.2);
static Json::Value big_sn("12345678901234567890");
static Json::Value big_si("-12345678901234567890");
static Json::Value big_u(0xFFFFFFFF);
static Json::Value bad_a(Json::arrayValue);
static Json::Value bad_o(Json::objectValue);

TEST(JsonTest, GetString) {
  std::string out;
  EXPECT_TRUE(GetStringFromJson(in_s, &out));
  EXPECT_EQ("foo", out);
  EXPECT_TRUE(GetStringFromJson(in_sn, &out));
  EXPECT_EQ("99", out);
  EXPECT_TRUE(GetStringFromJson(in_si, &out));
  EXPECT_EQ("-99", out);
  EXPECT_TRUE(GetStringFromJson(in_i, &out));
  EXPECT_EQ("-12", out);
  EXPECT_TRUE(GetStringFromJson(in_n, &out));
  EXPECT_EQ("12", out);
  EXPECT_TRUE(GetStringFromJson(in_u, &out));
  EXPECT_EQ("34", out);
  EXPECT_TRUE(GetStringFromJson(in_b, &out));
  EXPECT_EQ("true", out);
  // Not supported here yet.
  EXPECT_FALSE(GetStringFromJson(bad_a, &out));
  EXPECT_FALSE(GetStringFromJson(bad_o, &out));
}

TEST(JsonTest, GetInt) {
  int out;
  EXPECT_TRUE(GetIntFromJson(in_sn, &out));
  EXPECT_EQ(99, out);
  EXPECT_TRUE(GetIntFromJson(in_si, &out));
  EXPECT_EQ(-99, out);
  EXPECT_TRUE(GetIntFromJson(in_n, &out));
  EXPECT_EQ(12, out);
  EXPECT_TRUE(GetIntFromJson(in_i, &out));
  EXPECT_EQ(-12, out);
  EXPECT_TRUE(GetIntFromJson(in_u, &out));
  EXPECT_EQ(34, out);
  EXPECT_TRUE(GetIntFromJson(in_b, &out));
  EXPECT_EQ(1, out);
  EXPECT_FALSE(GetIntFromJson(in_s, &out));
  EXPECT_FALSE(GetIntFromJson(big_sn, &out));
  EXPECT_FALSE(GetIntFromJson(big_si, &out));
  EXPECT_FALSE(GetIntFromJson(big_u, &out));
  EXPECT_FALSE(GetIntFromJson(bad_a, &out));
  EXPECT_FALSE(GetIntFromJson(bad_o, &out));
}

TEST(JsonTest, GetUInt) {
  unsigned int out;
  EXPECT_TRUE(GetUIntFromJson(in_sn, &out));
  EXPECT_EQ(99U, out);
  EXPECT_TRUE(GetUIntFromJson(in_n, &out));
  EXPECT_EQ(12U, out);
  EXPECT_TRUE(GetUIntFromJson(in_u, &out));
  EXPECT_EQ(34U, out);
  EXPECT_TRUE(GetUIntFromJson(in_b, &out));
  EXPECT_EQ(1U, out);
  EXPECT_TRUE(GetUIntFromJson(big_u, &out));
  EXPECT_EQ(0xFFFFFFFFU, out);
  EXPECT_FALSE(GetUIntFromJson(in_s, &out));
  // TODO: Fail reading negative strings.
  // EXPECT_FALSE(GetUIntFromJson(in_si, &out));
  EXPECT_FALSE(GetUIntFromJson(in_i, &out));
  EXPECT_FALSE(GetUIntFromJson(big_sn, &out));
  EXPECT_FALSE(GetUIntFromJson(big_si, &out));
  EXPECT_FALSE(GetUIntFromJson(bad_a, &out));
  EXPECT_FALSE(GetUIntFromJson(bad_o, &out));
}

TEST(JsonTest, GetBool) {
  bool out;
  EXPECT_TRUE(GetBoolFromJson(in_sb, &out));
  EXPECT_EQ(true, out);
  EXPECT_TRUE(GetBoolFromJson(in_n, &out));
  EXPECT_EQ(true, out);
  EXPECT_TRUE(GetBoolFromJson(in_i, &out));
  EXPECT_EQ(true, out);
  EXPECT_TRUE(GetBoolFromJson(in_u, &out));
  EXPECT_EQ(true, out);
  EXPECT_TRUE(GetBoolFromJson(in_b, &out));
  EXPECT_EQ(true, out);
  EXPECT_TRUE(GetBoolFromJson(big_u, &out));
  EXPECT_EQ(true, out);
  EXPECT_FALSE(GetBoolFromJson(in_s, &out));
  EXPECT_FALSE(GetBoolFromJson(in_sn, &out));
  EXPECT_FALSE(GetBoolFromJson(in_si, &out));
  EXPECT_FALSE(GetBoolFromJson(big_sn, &out));
  EXPECT_FALSE(GetBoolFromJson(big_si, &out));
  EXPECT_FALSE(GetBoolFromJson(bad_a, &out));
  EXPECT_FALSE(GetBoolFromJson(bad_o, &out));
}

TEST(JsonTest, GetDouble) {
  double out;
  EXPECT_TRUE(GetDoubleFromJson(in_sn, &out));
  EXPECT_EQ(99, out);
  EXPECT_TRUE(GetDoubleFromJson(in_si, &out));
  EXPECT_EQ(-99, out);
  EXPECT_TRUE(GetDoubleFromJson(in_sd, &out));
  EXPECT_EQ(1.2, out);
  EXPECT_TRUE(GetDoubleFromJson(in_n, &out));
  EXPECT_EQ(12, out);
  EXPECT_TRUE(GetDoubleFromJson(in_i, &out));
  EXPECT_EQ(-12, out);
  EXPECT_TRUE(GetDoubleFromJson(in_u, &out));
  EXPECT_EQ(34, out);
  EXPECT_TRUE(GetDoubleFromJson(in_b, &out));
  EXPECT_EQ(1, out);
  EXPECT_TRUE(GetDoubleFromJson(in_d, &out));
  EXPECT_EQ(1.2, out);
  EXPECT_FALSE(GetDoubleFromJson(in_s, &out));
}

TEST(JsonTest, GetFromArray) {
  Json::Value a, out;
  a.append(in_s);
  a.append(in_i);
  a.append(in_u);
  a.append(in_b);
  EXPECT_TRUE(GetValueFromJsonArray(a, 0, &out));
  EXPECT_TRUE(GetValueFromJsonArray(a, 3, &out));
  EXPECT_FALSE(GetValueFromJsonArray(a, 99, &out));
  EXPECT_FALSE(GetValueFromJsonArray(a, 0xFFFFFFFF, &out));
}

TEST(JsonTest, GetFromObject) {
  Json::Value o, out;
  o["string"] = in_s;
  o["int"] = in_i;
  o["uint"] = in_u;
  o["bool"] = in_b;
  EXPECT_TRUE(GetValueFromJsonObject(o, "int", &out));
  EXPECT_TRUE(GetValueFromJsonObject(o, "bool", &out));
  EXPECT_FALSE(GetValueFromJsonObject(o, "foo", &out));
  EXPECT_FALSE(GetValueFromJsonObject(o, "", &out));
}

TEST(JsonTest, VectorToArray) {
  std::vector<std::string> in;
  Json::Value out;
  in.push_back("a");
  in.push_back("b");
  in.push_back("c");
  out = StringVectorToJsonValue(in);
  EXPECT_EQ(in.size(), out.size());
  for (Json::Value::ArrayIndex i = 0; i < in.size(); ++i) {
    EXPECT_EQ(in[i], out[i].asString());
  }
}

TEST(JsonTest, ArrayToVector) {
  Json::Value in(Json::arrayValue);
  std::vector<std::string> out;
  in.append("a");
  in.append("b");
  in.append("c");
  EXPECT_TRUE(JsonValueToStringVector(in, &out));
  EXPECT_EQ(in.size(), out.size());
  for (Json::Value::ArrayIndex i = 0; i < in.size(); ++i) {
    EXPECT_EQ(in[i].asString(), out[i]);
  }
}